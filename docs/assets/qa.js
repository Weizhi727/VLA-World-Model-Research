// 站內問答：預設用全站段落做關鍵字檢索（不需金鑰）；
// 讀者若在設定裡填入自己的 Anthropic API 金鑰，就把檢索到的段落交給 Claude 生成回答。
(function () {
  var INDEX = window.SITE_INDEX || [];
  var SDK_URL = 'https://esm.sh/@anthropic-ai/sdk@0.130.0';
  var MODEL = 'claude-opus-5-5';
  var KEY_STORE = 'qa-anthropic-key';
  var SUGGEST = [
    'VLA 和世界模型差在哪？',
    '雙系統架構是什麼？',
    '世界模型在推論時真的有用到嗎？',
    '合成資料怎麼確保物理正確？',
    'π0 是怎麼訓練的？',
    '智平方的 FiS-VLA 有什麼特別？'
  ];
  // 中英混用的常見同義詞，檢索前先展開
  var ALIAS = [
    [/world\s*models?/gi, ' 世界模型 '], [/\bwm\b/gi, ' 世界模型 '], [/快慢腦|大小腦/g, ' 雙系統 '],
    [/dual[\s-]*system/gi, ' 雙系統 '], [/synthetic\s*data/gi, ' 合成資料 '], [/pi\s*0/gi, ' π0 '], [/差在哪|差異|區別|不同/g, ' 差別 ']
  ];

  // ---------- 檢索 ----------
  function tokens(s) {
    s = s.toLowerCase();
    ALIAS.forEach(function (a) { s = s.replace(a[0], a[1]); });
    var out = [];
    var words = s.match(/[a-z0-9π][a-z0-9π.\-*]*/g) || [];
    words.forEach(function (w) { w = w.replace(/[.\-]+$/, ''); if (w.length > 1 || /\d|π/.test(w)) out.push(w); });
    var runs = s.match(/[㐀-鿿]+/g) || [];
    runs.forEach(function (r) {
      if (r.length === 1) out.push(r);
      for (var i = 0; i + 1 < r.length; i++) {
        var bg = r.slice(i, i + 2);
        if (!FUNC.test(bg)) out.push(bg);
      }
    });
    return out;
  }
  // 含虛詞的二字組多半是跨詞邊界的雜訊（「的控」「率多」）
  var FUNC = /[的了嗎呢麼什怎哪吧請問與和及或嗎吗]/;
  var STOP = { '什麼': 1, '怎麼': 1, '為什': 1, '麼是': 1, '是什': 1, '哪些': 1, '如何': 1, '有沒': 1, '沒有': 1, '可以': 1, '一下': 1, '請問': 1, '差在': 1, '在哪': 1, '多少': 1, '有用': 1, '真的': 1, '特別': 1, 'the': 1, 'and': 1, 'is': 1, 'what': 1, 'how': 1 };

  var docs = INDEX.map(function (d) {
    var tf = {}, head = {};
    tokens(d.x).forEach(function (t) { tf[t] = (tf[t] || 0) + 1; });
    tokens(d.s + ' ' + d.t).forEach(function (t) { head[t] = 1; });
    return { d: d, tf: tf, head: head, len: d.x.length };
  });
  var avgLen = docs.reduce(function (a, b) { return a + b.len; }, 0) / Math.max(docs.length, 1);
  var df = {};
  docs.forEach(function (doc) { Object.keys(doc.tf).forEach(function (t) { df[t] = (df[t] || 0) + 1; }); });

  function search(q, k) {
    var qt = tokens(q).filter(function (t) { return !STOP[t]; });
    var uniq = Array.from(new Set(qt));
    if (!uniq.length) return [];
    var N = docs.length, w = {}, wsum = 0;
    uniq.forEach(function (t) {
      w[t] = Math.log(1 + (N - (df[t] || 0) + 0.5) / ((df[t] || 0) + 0.5));
      if (!/[\u3400-\u9fff]/.test(t)) w[t] *= 2;
      wsum += w[t];
    });
    var scored = docs.map(function (doc) {
      var s = 0, hit = 0;
      uniq.forEach(function (t) {
        var f = doc.tf[t] || 0, n = df[t] || 0;
        if (!f && !doc.head[t]) return;
        hit += w[t];
        var idf = w[t]; // 英文詞與型號（FiS-VLA、π0）比中文二字組更有鑑別力，權重加倍
        s += idf * (f * 2.2) / (f + 1.2 * (0.25 + 0.75 * doc.len / avgLen));
        if (doc.head[t]) s += idf * 1.5;
      });
      // 問題裡的關鍵詞命中越多越好（依鑑別力加權），避免只靠一個常見詞拿高分
      return { doc: doc, score: s * Math.pow(hit / wsum, 1.5) };
    }).filter(function (r) { return r.score > 0; });
    scored.sort(function (a, b) { return b.score - a.score; });
    return scored.slice(0, k).map(function (r) { r.terms = uniq; return r; });
  }

  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function snippet(text, terms, size) {
    var flat = text.replace(/\n+/g, ' ');
    var low = flat.toLowerCase(), best = 0, bestHits = -1;
    for (var i = 0; i < flat.length; i += 20) {
      var win = low.slice(i, i + size), hits = 0;
      terms.forEach(function (t) { if (win.indexOf(t) >= 0) hits++; });
      if (hits > bestHits) { bestHits = hits; best = i; }
    }
    var part = flat.slice(best, best + size);
    var html = esc(part);
    var marks = terms.filter(function (t) { return t.length > 1; }).sort(function (a, b) { return b.length - a.length; });
    if (marks.length) {
      var re = new RegExp('(' + marks.map(function (t) { return esc(t).replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }).join('|') + ')', 'gi');
      html = html.replace(re, '<mark>$1</mark>');
    }
    return (best > 0 ? '…' : '') + html + (best + size < flat.length ? '…' : '');
  }

  function href(d) { return d.p + '.html' + (d.a ? '#' + d.a : ''); }

  // ---------- 介面 ----------
  var fab = document.createElement('button');
  fab.className = 'qa-fab';
  fab.type = 'button';
  fab.setAttribute('aria-label', '開啟站內問答');
  fab.innerHTML = '<span aria-hidden="true">?</span>問答';

  var panel = document.createElement('section');
  panel.className = 'qa-panel';
  panel.setAttribute('aria-label', '站內問答');
  panel.hidden = true;
  panel.innerHTML =
    '<header><b>站內問答</b><span class="qa-mode"></span>' +
    '<button type="button" class="qa-set" aria-label="設定">⚙</button>' +
    '<button type="button" class="qa-x" aria-label="關閉">×</button></header>' +
    '<div class="qa-log" aria-live="polite"></div>' +
    '<div class="qa-settings" hidden>' +
    '<p><b>用 Claude 生成回答（選用）</b></p>' +
    '<p>預設模式只在本站內容中找出最相關的段落。填入你自己的 <a class="ext" href="https://console.anthropic.com/settings/keys" target="_blank" rel="noopener">Anthropic API 金鑰</a> 後，會把找到的段落交給 Claude，整理成一段有出處的回答。</p>' +
    '<p class="qa-note">金鑰只存在這個瀏覽器（localStorage），直接從你的瀏覽器送到 api.anthropic.com，不經過任何其他伺服器。費用由你的帳號支付。請勿在公用電腦上使用。</p>' +
    '<input type="password" class="qa-key" placeholder="sk-ant-…" autocomplete="off" spellcheck="false">' +
    '<div class="qa-row"><button type="button" class="qa-save">儲存</button><button type="button" class="qa-clear">清除金鑰</button></div>' +
    '</div>' +
    '<form class="qa-form"><textarea rows="1" placeholder="問一個關於 VLA 或世界模型的問題…" aria-label="輸入問題"></textarea>' +
    '<button type="submit" aria-label="送出">↑</button></form>';

  document.body.appendChild(fab);
  document.body.appendChild(panel);

  var log = panel.querySelector('.qa-log');
  var form = panel.querySelector('.qa-form');
  var input = form.querySelector('textarea');
  var settings = panel.querySelector('.qa-settings');
  var keyInput = panel.querySelector('.qa-key');
  var modeTag = panel.querySelector('.qa-mode');
  var history = []; // 生成模式的對話紀錄（只存文字）
  var busy = false;

  function getKey() { try { return localStorage.getItem(KEY_STORE) || ''; } catch (e) { return ''; } }
  function setKey(v) { try { v ? localStorage.setItem(KEY_STORE, v) : localStorage.removeItem(KEY_STORE); } catch (e) {} }
  function refreshMode() {
    var on = !!getKey();
    modeTag.textContent = on ? 'Claude 生成' : '站內檢索';
    modeTag.classList.toggle('on', on);
  }

  function add(cls, html) {
    var el = document.createElement('div');
    el.className = 'qa-msg ' + cls;
    el.innerHTML = html;
    log.appendChild(el);
    log.scrollTop = log.scrollHeight;
    return el;
  }

  function welcome() {
    var chips = SUGGEST.map(function (s) { return '<button type="button" class="qa-chip">' + esc(s) + '</button>'; }).join('');
    add('bot', '<p>我會在這個網站的 11 個章節裡找答案，並附上段落連結。可以先試試：</p><div class="qa-chips">' + chips + '</div>');
  }

  function sourcesHtml(hits, withSnippet) {
    return '<ol class="qa-src">' + hits.map(function (h) {
      var d = h.doc.d;
      return '<li><a href="' + href(d) + '"><b>' + esc(d.s) + '</b><small>' + esc(d.t) + '</small></a>' +
        (withSnippet ? '<p>' + snippet(d.x, h.terms, 110) + '</p>' : '') + '</li>';
    }).join('') + '</ol>';
  }

  function answerRetrieval(q) {
    var hits = search(q, 4);
    if (!hits.length) {
      add('bot', '<p>本站內容裡找不到相關段落。可以換個說法，或到 <a href="glossary.html">名詞速查</a> 看看有沒有對應的術語。</p>');
      return;
    }
    add('bot', '<p>最相關的段落：</p>' + sourcesHtml(hits, true) +
      (getKey() ? '' : '<p class="qa-note">想要整理好的回答？點右上角 ⚙ 設定 Claude 生成模式。</p>'));
  }

  // 生成回答的極簡 Markdown：粗體、行內程式碼、清單、[n] 出處
  function md(text, hits) {
    var h = esc(text)
      .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\[(\d+)\]/g, function (m, n) {
        var hit = hits[+n - 1];
        return hit ? '<a class="qa-cite" href="' + href(hit.doc.d) + '" title="' + esc(hit.doc.d.s) + '">' + n + '</a>' : m;
      });
    var lines = h.split('\n'), out = [], list = null;
    lines.forEach(function (l) {
      var m = l.match(/^\s*(?:[-*•]|\d+[.)])\s+(.*)$/);
      if (m) { if (!list) { list = []; } list.push('<li>' + m[1] + '</li>'); return; }
      if (list) { out.push('<ul>' + list.join('') + '</ul>'); list = null; }
      if (l.trim()) out.push('<p>' + l.replace(/^#+\s*/, '') + '</p>');
    });
    if (list) out.push('<ul>' + list.join('') + '</ul>');
    return out.join('');
  }

  var sdkPromise = null;
  function loadSdk() {
    if (!sdkPromise) sdkPromise = import(SDK_URL).then(function (m) { return m.default || m.Anthropic; });
    return sdkPromise;
  }

  var SYSTEM = '你是「VLA × 世界模型 調研」網站的問答助理，讀者是想入門的工程師。' +
    '只根據使用者訊息裡附上的網站段落回答，用繁體中文，先講結論再補細節，重點用粗體。' +
    '每個論點後面用 [編號] 標出依據的段落。段落裡沒有的資訊，直接說本站沒有寫到，不要自行補充或猜測數字。' +
    '回答控制在 250 字以內，除非使用者要求更詳細。';

  function answerClaude(q) {
    var prev = history.length ? history[history.length - 2].q : '';
    var hits = search(q + ' ' + prev, 6);
    if (!hits.length) hits = search(q, 6);
    var ctx = hits.map(function (h, i) {
      var d = h.doc.d;
      return '[' + (i + 1) + '] 〈' + d.t + '〉' + d.s + '\n' + d.x.slice(0, 2400);
    }).join('\n\n');
    var bubble = add('bot', '<p class="qa-wait">正在讀相關段落並整理回答…</p>');
    var messages = [];
    history.slice(-4).forEach(function (m) { messages.push({ role: m.role, content: m.text }); });
    messages.push({ role: 'user', content: '網站段落：\n\n' + (ctx || '（沒有找到相關段落）') + '\n\n問題：' + q });

    return loadSdk().then(function (Anthropic) {
      var client = new Anthropic({ apiKey: getKey(), dangerouslyAllowBrowser: true });
      var stream = client.beta.messages.stream({
        model: MODEL,
        max_tokens: 4000,
        output_config: { effort: 'low' },
        betas: ['server-side-fallback-2026-07-01'],
        fallbacks: 'default',
        system: SYSTEM,
        messages: messages
      });
      var text = '';
      stream.on('text', function (delta) {
        text += delta;
        bubble.innerHTML = md(text, hits);
        log.scrollTop = log.scrollHeight;
      });
      return stream.finalMessage().then(function (msg) {
        if (msg.stop_reason === 'refusal') {
          bubble.innerHTML = '<p>這個問題 Claude 無法回答。以下是站內最相關的段落：</p>' + sourcesHtml(hits.slice(0, 4), true);
          return;
        }
        bubble.innerHTML = md(text, hits) + '<details class="qa-more"><summary>參考段落</summary>' + sourcesHtml(hits, false) + '</details>';
        history.push({ role: 'user', text: q, q: q }, { role: 'assistant', text: text });
        log.scrollTop = log.scrollHeight;
      });
    }).catch(function (err) {
      var status = err && err.status;
      var why = status === 401 ? '金鑰無效，請到 ⚙ 重新設定。'
        : status === 429 ? '請求太頻繁或額度不足，稍後再試。'
        : status ? 'API 回傳錯誤（' + status + '）。'
        : '連不上 Claude API（可能是網路或瀏覽器擋住了外部腳本）。';
      bubble.innerHTML = '<p>' + why + '先附上站內最相關的段落：</p>' + sourcesHtml(hits.slice(0, 4), true);
    });
  }

  function ask(q) {
    q = q.trim();
    if (!q || busy) return;
    add('me', '<p>' + esc(q) + '</p>');
    input.value = '';
    autosize();
    if (getKey()) {
      busy = true;
      form.classList.add('busy');
      answerClaude(q).then(function () { busy = false; form.classList.remove('busy'); });
    } else {
      answerRetrieval(q);
    }
  }

  function autosize() { input.style.height = 'auto'; input.style.height = Math.min(input.scrollHeight, 120) + 'px'; }

  function open(v) {
    panel.hidden = !v;
    fab.hidden = v;
    document.body.classList.toggle('qa-open', v);
    if (v) { if (!log.children.length) welcome(); input.focus(); }
  }

  fab.addEventListener('click', function () { open(true); });
  panel.querySelector('.qa-x').addEventListener('click', function () { open(false); });
  panel.querySelector('.qa-set').addEventListener('click', function () {
    settings.hidden = !settings.hidden;
    if (!settings.hidden) keyInput.value = getKey();
  });
  panel.querySelector('.qa-save').addEventListener('click', function () {
    setKey(keyInput.value.trim()); refreshMode(); settings.hidden = true;
    add('bot', '<p>' + (getKey() ? '已切換到 Claude 生成模式。' : '已切回站內檢索模式。') + '</p>');
  });
  panel.querySelector('.qa-clear').addEventListener('click', function () {
    setKey(''); keyInput.value = ''; refreshMode(); settings.hidden = true; history = [];
    add('bot', '<p>金鑰已清除，回到站內檢索模式。</p>');
  });
  log.addEventListener('click', function (e) {
    var chip = e.target.closest('.qa-chip');
    if (chip) ask(chip.textContent);
  });
  form.addEventListener('submit', function (e) { e.preventDefault(); ask(input.value); });
  input.addEventListener('input', autosize);
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); ask(input.value); }
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) open(false); });

  refreshMode();
})();

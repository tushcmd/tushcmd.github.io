(function () {
  var root = document.documentElement;

  // Theme toggle, remembered across visits.
  var themeBtn = document.getElementById("theme");
  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      var current = root.getAttribute("data-theme");
      if (!current) current = window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
      var next = current === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("theme", next); } catch (e) {}
    });
  }

  // Hamburger menu.
  var menuBtn = document.getElementById("menu-btn");
  var menu = document.getElementById("menu");
  if (menuBtn && menu) {
    var setMenu = function (open) {
      menu.classList.toggle("open", open);
      menuBtn.classList.toggle("open", open);
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
      menuBtn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    };
    menuBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      setMenu(!menu.classList.contains("open"));
    });
    document.addEventListener("click", function (e) {
      if (menu.classList.contains("open") && !menu.contains(e.target)) setMenu(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menu.classList.contains("open")) { setMenu(false); menuBtn.focus(); }
    });
  }

  // Local time in Nairobi.
  var clocks = document.querySelectorAll("#clock, .clock");
  if (clocks.length && window.Intl) {
    var fmt = new Intl.DateTimeFormat("en-GB", { timeZone: "Africa/Nairobi", hour: "2-digit", minute: "2-digit", hour12: false });
    var tick = function () { var t = fmt.format(new Date()) + " EAT"; clocks.forEach(function (c) { c.textContent = t; }); };
    tick();
    setInterval(tick, 30000);
  }

  // Copy buttons on code blocks.
  document.querySelectorAll(".code .copy").forEach(function (b) {
    b.addEventListener("click", function () {
      var code = b.closest(".code").querySelector("code");
      var text = code ? code.textContent : "";
      var done = function () { b.textContent = "Copied"; setTimeout(function () { b.textContent = "Copy"; }, 1500); };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, function () {});
      }
    });
  });

  // Reading progress on articles.
  var bar = document.getElementById("progress");
  if (bar) {
    var update = function () {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.transform = "scaleX(" + (h > 0 ? Math.min(1, window.scrollY / h) : 0) + ")";
    };
    window.addEventListener("scroll", update, { passive: true });
    update();
  }

  // Scroll reveal. Anything already on screen stays put; only content below the fold animates in.
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.08, rootMargin: "0px 0px -4% 0px" });
    var sel = ".main .list > li, .main .defs > div, .main .prose > *, .main .section, .main .facts, .main .next, .main .more, .foot";
    document.querySelectorAll(sel).forEach(function (el) {
      if (el.getBoundingClientRect().top < window.innerHeight * 0.98) return;
      var idx = Array.prototype.indexOf.call(el.parentNode.children, el);
      el.style.setProperty("--d", Math.min(Math.max(idx, 0), 5) * 50 + "ms");
      el.classList.add("reveal");
      io.observe(el);
    });
  }
})();

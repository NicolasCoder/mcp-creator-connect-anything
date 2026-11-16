/**
 * ⚡ MCP Creator — Connect Anything: DOM & Shadow-DOM Native Bypass Engine (dom_bypass.js)
 * ========================================================================================
 * Battle-tested JavaScript runtime injected via Chrome DevTools Protocol (CDP)
 * to bypass modern SPA barriers (React 18/19 Fiber, Lit / Spectrum Web Components,
 * Angular Material, Vue 3, ProseMirror) and enforce the Triple Audio Silence Shield.
 */

window.__MCP_CREATOR_BYPASS__ = (() => {
  /**
   * 1. RECURSIVE SHADOW-DOM PIERCING (`querySelectorDeep` & `querySelectorAllDeep`)
   * Traverses open Shadow Roots and nested Custom Elements (`<sp-*>`, `<ms-*>`, `<flow-*>`, etc.)
   * Supports comma-separated fallback selectors.
   */
  function querySelectorAllDeep(selector, root = document) {
    const results = [];
    if (!root || !selector) return results;

    const selectors = selector
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);

    function collect(node) {
      if (!node) return;
      for (const sel of selectors) {
        try {
          if (node.querySelectorAll) {
            const matched = node.querySelectorAll(sel);
            for (const el of matched) {
              if (!results.includes(el)) results.push(el);
            }
          }
        } catch (e) {
          // Ignore Playwright-specific pseudo-selectors when running in raw DOM
        }
      }
      if (!node.querySelectorAll) return;
      const allNodes = node.querySelectorAll("*");
      for (const el of allNodes) {
        if (el.shadowRoot) {
          collect(el.shadowRoot);
        }
      }
    }

    collect(root);
    return results;
  }

  function querySelectorDeep(selector, root = document) {
    const all = querySelectorAllDeep(selector, root);
    return all.length > 0 ? all[0] : null;
  }

  /**
   * 2. REACT FIBER / VUE / ANGULAR NATIVE VALUE SETTER (`setReactInputValue`)
   * Why `.value = "foo"` fails in React/Vue/Angular:
   * React overrides the value setter on the instance to track internal state (`_valueTracker`).
   * Calling the native prototype setter from `HTMLInputElement.prototype` or `HTMLTextAreaElement.prototype`
   * and dispatching a bubbling `InputEvent` forces React's synthetic event system to commit the new state.
   */
  function setReactInputValue(elementOrSelector, newValue) {
    const el =
      typeof elementOrSelector === "string"
        ? querySelectorDeep(elementOrSelector)
        : elementOrSelector;
    if (!el) return { ok: false, error: "Element not found" };

    try {
      el.focus();

      // ContentEditable / ProseMirror / Lexical rich-text editors
      if (el.isContentEditable || el.getAttribute("contenteditable") === "true") {
        el.innerHTML = "";
        const p = document.createElement("p");
        p.textContent = String(newValue);
        el.appendChild(p);
        el.dispatchEvent(
          new InputEvent("input", {
            bubbles: true,
            composed: true,
            inputType: "insertText",
            data: String(newValue),
          })
        );
        el.dispatchEvent(new Event("change", { bubbles: true, composed: true }));
        return { ok: true, mode: "contenteditable" };
      }

      const proto =
        el.tagName.toLowerCase() === "textarea"
          ? window.HTMLTextAreaElement.prototype
          : window.HTMLInputElement.prototype;

      const nativeSetter = Object.getOwnPropertyDescriptor(proto, "value")?.set;
      const tracker = el._valueTracker;
      if (tracker) {
        tracker.setValue(el.value);
      }

      if (nativeSetter) {
        nativeSetter.call(el, String(newValue));
      } else {
        el.value = String(newValue);
      }

      el.dispatchEvent(
        new InputEvent("input", {
          bubbles: true,
          composed: true,
          data: String(newValue),
          inputType: "insertText",
        })
      );
      el.dispatchEvent(new Event("change", { bubbles: true, composed: true }));
      el.blur();
      return { ok: true, mode: "native_prototype_setter" };
    } catch (err) {
      return { ok: false, error: String(err) };
    }
  }

  /**
   * 3. WEB COMPONENT & RANGE SLIDER BYPASS (`setSliderValue`)
   * Handles native `<input type="range">`, Adobe Spectrum `<sp-slider>`,
   * Angular Material `<mat-slider>`, and Radix/Shadcn sliders.
   */
  function setSliderValue(elementOrSelector, numericValue) {
    const el =
      typeof elementOrSelector === "string"
        ? querySelectorDeep(elementOrSelector)
        : elementOrSelector;
    if (!el) return { ok: false, error: "Slider element not found" };

    try {
      const targetVal = Number(numericValue);
      // Check if an inner <input type="range"> exists inside Shadow DOM
      const innerRange =
        el.tagName.toLowerCase() === "input"
          ? el
          : querySelectorDeep('input[type="range"]', el.shadowRoot || el) || el;

      const nativeSetter = Object.getOwnPropertyDescriptor(
        window.HTMLInputElement.prototype,
        "value"
      )?.set;

      if (innerRange && innerRange.tagName?.toLowerCase() === "input" && nativeSetter) {
        nativeSetter.call(innerRange, String(targetVal));
      }

      el.value = targetVal;
      if (innerRange && innerRange !== el) {
        innerRange.value = targetVal;
      }

      for (const node of [innerRange, el]) {
        if (!node) continue;
        node.dispatchEvent(new Event("input", { bubbles: true, composed: true }));
        node.dispatchEvent(new Event("change", { bubbles: true, composed: true }));
      }

      const rect = el.getBoundingClientRect();
      return {
        ok: true,
        value: targetVal,
        boundingBox: {
          x: rect.x,
          y: rect.y,
          width: rect.width,
          height: rect.height,
        },
      };
    } catch (err) {
      return { ok: false, error: String(err) };
    }
  }

  /**
   * 4. BLOB / MEDIA URI EXTRACTOR (`extractBlobAsBase64`)
   * Layer 2 of the Triple-Capture Engine: fetches `blob:https://...` or `data:...`
   * inside the authenticated page context and returns raw Base64 + MIME type.
   */
  async function extractBlobAsBase64(blobOrDataUrl) {
    try {
      if (!blobOrDataUrl) return { ok: false, error: "Empty URL" };
      if (blobOrDataUrl.startsWith("data:")) {
        const [header, b64] = blobOrDataUrl.split(";base64,");
        return {
          ok: true,
          mimeType: header.replace("data:", ""),
          base64: b64 || "",
          source: "data_uri",
        };
      }
      const response = await fetch(blobOrDataUrl);
      const blob = await response.blob();
      return await new Promise((resolve) => {
        const reader = new FileReader();
        reader.onloadend = () => {
          const dataUrl = String(reader.result || "");
          const b64 = dataUrl.includes(";base64,")
            ? dataUrl.split(";base64,")[1]
            : "";
          resolve({
            ok: true,
            mimeType: blob.type || "application/octet-stream",
            sizeBytes: blob.size,
            base64: b64,
            source: "blob_fetch",
          });
        };
        reader.onerror = (e) =>
          resolve({ ok: false, error: String(e), source: "blob_fetch" });
        reader.readAsDataURL(blob);
      });
    } catch (err) {
      return { ok: false, error: String(err) };
    }
  }

  /**
   * 5. TRIPLE AUDIO SILENCE SHIELD (`installAudioSilenceShield`)
   * Guarantees 0% audio leakage to the user's PC speakers even when the web app
   * auto-plays generated audio/video previews via `<audio>`, `<video>`, or WebAudio API.
   */
  function installAudioSilenceShield() {
    try {
      Object.defineProperty(HTMLMediaElement.prototype, "muted", {
        get: () => true,
        set: () => {},
        configurable: true,
      });
      Object.defineProperty(HTMLMediaElement.prototype, "volume", {
        get: () => 0,
        set: () => {},
        configurable: true,
      });
      if (!HTMLMediaElement.prototype.__mcpOrigPlay) {
        HTMLMediaElement.prototype.__mcpOrigPlay = HTMLMediaElement.prototype.play;
        HTMLMediaElement.prototype.play = function () {
          try {
            this.pause();
          } catch (e) {}
          return Promise.resolve();
        };
      }
      document.querySelectorAll("audio, video").forEach((el) => {
        try {
          el.pause();
        } catch (e) {}
      });
    } catch (e) {}

    try {
      if (
        typeof AudioNode !== "undefined" &&
        !AudioNode.prototype.__mcpOrigConnect
      ) {
        const origConnect = AudioNode.prototype.connect;
        AudioNode.prototype.__mcpOrigConnect = origConnect;
        AudioNode.prototype.connect = function (destination, ...rest) {
          try {
            const isDest =
              destination &&
              ((typeof AudioDestinationNode !== "undefined" &&
                destination instanceof AudioDestinationNode) ||
                (this.context && destination === this.context.destination));
            if (isDest && this.context) {
              const ctx = this.context;
              if (!ctx.__mcpZeroGain) {
                const g = ctx.createGain();
                g.gain.value = 0;
                try {
                  g.gain.setValueAtTime(0, 0);
                  Object.defineProperty(g.gain, "value", {
                    get: () => 0,
                    set: () => {},
                  });
                } catch (e) {}
                origConnect.call(g, destination);
                ctx.__mcpZeroGain = g;
              }
              return origConnect.call(this, ctx.__mcpZeroGain, ...rest);
            }
          } catch (e) {}
          return origConnect.call(this, destination, ...rest);
        };
      }
    } catch (e) {}
    return { ok: true };
  }

  /**
   * 6. AUTO-HEALING DOM & SHADOW-DOM X-RAY (`dumpInteractiveElementsForHealing`)
   * Recursively walks the entire DOM + Shadow DOM tree and extracts every interactive
   * button, input, file uploader, custom tag, alert/toast, and bounding box so AI agents
   * can self-heal `selectors.json` in seconds when a platform updates its UI.
   */
  function dumpInteractiveElementsForHealing(maxItems = 160) {
    function walkShadow(root, depth = 0, out = []) {
      if (!root || !root.querySelectorAll || depth > 8) return out;
      for (const el of root.querySelectorAll("*")) {
        const tag = el.tagName ? el.tagName.toLowerCase() : "";
        const id = el.id || "";
        const testid =
          (el.getAttribute &&
            (el.getAttribute("data-testid") ||
              el.getAttribute("data-test-id") ||
              el.getAttribute("data-cy"))) ||
          "";
        const role = (el.getAttribute && el.getAttribute("role")) || "";
        const aria =
          (el.getAttribute &&
            (el.getAttribute("aria-label") ||
              el.getAttribute("label") ||
              el.getAttribute("title"))) ||
          "";
        const placeholder =
          (el.getAttribute && el.getAttribute("placeholder")) || "";
        const type = (el.getAttribute && el.getAttribute("type")) || "";
        const text = (el.innerText || el.textContent || "")
          .trim()
          .replace(/\s+/g, " ")
          .slice(0, 90);
        const classes = (el.className || "").toString().slice(0, 80);
        const rect = el.getBoundingClientRect
          ? el.getBoundingClientRect()
          : { width: 0, height: 0, x: 0, y: 0 };
        const visible =
          (rect.width > 0 && rect.height > 0) ||
          type === "file" ||
          id.toLowerCase().includes("upload");

        out.push({
          tag,
          id,
          testid,
          role,
          aria,
          placeholder,
          type,
          text,
          classes,
          visible,
          inShadowDom: depth > 0,
          rect: {
            x: Math.round(rect.x || 0),
            y: Math.round(rect.y || 0),
            w: Math.round(rect.width || 0),
            h: Math.round(rect.height || 0),
          },
        });

        if (el.shadowRoot) {
          walkShadow(el.shadowRoot, depth + 1, out);
        }
      }
      return out;
    }

    const all = walkShadow(document);
    const interactive = all
      .filter(
        (x) =>
          (x.tag.includes("button") ||
            x.tag === "a" ||
            x.tag === "input" ||
            x.tag === "textarea" ||
            x.tag === "select" ||
            x.tag.includes("slider") ||
            x.tag.includes("picker") ||
            x.tag.includes("switch") ||
            x.role === "button" ||
            x.role === "menuitem" ||
            x.role === "tab" ||
            x.role === "option" ||
            x.testid ||
            x.aria ||
            x.placeholder) &&
          (x.visible || x.type === "file" || x.testid)
      )
      .slice(0, maxItems);

    const fileInputs = all.filter(
      (x) => x.tag === "input" && x.type === "file"
    );
    const testids = Array.from(
      new Set(all.map((x) => x.testid).filter(Boolean))
    ).sort();
    const customWebComponents = Array.from(
      new Set(all.map((x) => x.tag).filter((t) => t.includes("-")))
    ).sort();
    const alertsOrModals = all
      .filter(
        (x) =>
          x.visible &&
          (x.role === "alert" ||
            x.role === "dialog" ||
            x.testid.includes("error") ||
            x.testid.includes("modal") ||
            x.testid.includes("upsell") ||
            x.tag.includes("dialog") ||
            x.tag.includes("toast") ||
            x.tag.includes("snack"))
      )
      .slice(0, 25);

    return {
      title: document.title,
      url: window.location.href,
      totalNodesScanned: all.length,
      testids,
      customWebComponents,
      fileInputs,
      interactive,
      alertsOrModals,
    };
  }

  return {
    querySelectorDeep,
    querySelectorAllDeep,
    setReactInputValue,
    setSliderValue,
    extractBlobAsBase64,
    installAudioSilenceShield,
    dumpInteractiveElementsForHealing,
  };
})();

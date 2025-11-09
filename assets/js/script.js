document.addEventListener("DOMContentLoaded", () => {
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  initialiseCurrentYear();
  initialiseHeaderCondense();
  initialiseRevealAnimations(prefersReducedMotion);
  initialiseCounters();
  initialiseTiltCards(prefersReducedMotion);
  initialiseTimeline();
  initialiseCarousel(prefersReducedMotion);
  initialiseContactForm();
  initialiseInsightsModal();
  loadHeicImage();
});

function initialiseCurrentYear() {
  const target = document.querySelector("[data-current-year]");
  if (target) {
    target.textContent = new Date().getFullYear();
  }
}

function initialiseHeaderCondense() {
  const header = document.querySelector("[data-nav]");
  if (!header) return;

  const threshold = header.offsetHeight;

  const update = () => {
    if (window.scrollY > threshold) {
      header.classList.add("is-condensed");
    } else {
      header.classList.remove("is-condensed");
    }
  };

  update();
  window.addEventListener("scroll", update, { passive: true });
}

function initialiseRevealAnimations(prefersReducedMotion) {
  const revealElements = document.querySelectorAll(".reveal");
  if (!revealElements.length) return;

  if (prefersReducedMotion || !("IntersectionObserver" in window)) {
    revealElements.forEach((el) => el.classList.add("is-visible"));
    document.querySelectorAll(".hero__stat-value[data-count]").forEach((node) => {
      const value = Number(node.dataset.count || 0);
      node.textContent = value;
    });
    return;
  }

  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          if (entry.target.querySelectorAll) {
            entry.target
              .querySelectorAll(".hero__stat-value[data-count]")
              .forEach((node) => animateCounter(node));
          }
          obs.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.24 }
  );

  revealElements.forEach((el) => observer.observe(el));
}

function initialiseCounters() {
  const counters = document.querySelectorAll(".hero__stat-value[data-count]");
  counters.forEach((counter) => {
    counter.textContent = "0";
  });
}

function animateCounter(node) {
  const targetValue = Number(node.dataset.count || 0);
  if (!targetValue || node.dataset.countAnimated) return;

  const duration = 1600;
  const startTimestamp = performance.now();

  const tick = (now) => {
    const progress = Math.min((now - startTimestamp) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    node.textContent = Math.round(eased * targetValue).toLocaleString();
    if (progress < 1) {
      requestAnimationFrame(tick);
    } else {
      node.textContent = targetValue.toLocaleString();
      node.dataset.countAnimated = "true";
    }
  };

  requestAnimationFrame(tick);
}

function initialiseTiltCards(prefersReducedMotion) {
  if (prefersReducedMotion) return;
  const tiltNodes = document.querySelectorAll("[data-tilt]");
  tiltNodes.forEach((node) => {
    const strength = 12;
    let rafId = null;

    const handlePointerMove = (event) => {
      const rect = node.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      const dx = (event.clientX - cx) / rect.width;
      const dy = (event.clientY - cy) / rect.height;

      if (rafId) cancelAnimationFrame(rafId);
      rafId = requestAnimationFrame(() => {
        node.style.transform = `rotateX(${(-dy * strength).toFixed(2)}deg) rotateY(${(
          dx * strength
        ).toFixed(2)}deg) translateZ(0)`;
      });
    };

    const reset = () => {
      if (rafId) cancelAnimationFrame(rafId);
      node.style.transform = "";
    };

    node.addEventListener("pointermove", handlePointerMove);
    node.addEventListener("pointerleave", reset);
    node.addEventListener("pointercancel", reset);
  });
}

function initialiseTimeline() {
  const timeline = document.querySelector(".timeline");
  if (!timeline) return;

  const yearDisplay = timeline.querySelector(".timeline__year-display");
  const items = [...timeline.querySelectorAll(".timeline__item")];

  const setActive = (item) => {
    items.forEach((entry) => entry.classList.toggle("is-active", entry === item));
    if (item?.dataset?.year && yearDisplay) {
      yearDisplay.textContent = item.dataset.year;
    }
  };

  items.forEach((item) => {
    item.addEventListener("mouseenter", () => setActive(item));
    item.addEventListener("focus", () => setActive(item));
  });

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          setActive(entry.target);
        }
      });
    },
    { rootMargin: "-40% 0px -40% 0px", threshold: 0.15 }
  );

  items.forEach((item) => observer.observe(item));
}

function initialiseCarousel(prefersReducedMotion) {
  const carousel = document.querySelector("[data-carousel]");
  if (!carousel) return;

  const testimonials = carousel.querySelectorAll(".testimonial");
  if (!testimonials.length) return;

  let index = 0;
  let intervalId = null;

  const showIndex = (next) => {
    testimonials[index].classList.remove("is-active");
    index = (next + testimonials.length) % testimonials.length;
    testimonials[index].classList.add("is-active");
  };

  const next = () => showIndex(index + 1);
  const prev = () => showIndex(index - 1);

  const startAutoPlay = () => {
    if (prefersReducedMotion) return;
    stopAutoPlay();
    intervalId = setInterval(next, 7500);
  };

  const stopAutoPlay = () => {
    if (intervalId) clearInterval(intervalId);
    intervalId = null;
  };

  carousel.querySelector("[data-carousel-next]")?.addEventListener("click", () => {
    next();
    startAutoPlay();
  });

  carousel.querySelector("[data-carousel-prev]")?.addEventListener("click", () => {
    prev();
    startAutoPlay();
  });

  carousel.addEventListener("pointerenter", stopAutoPlay);
  carousel.addEventListener("pointerleave", startAutoPlay);

  testimonials[index].classList.add("is-active");
  startAutoPlay();
}

function initialiseContactForm() {
  const form = document.querySelector(".contact__form");
  if (!form) return;

  const statusNode = form.querySelector(".form-message");
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const missingFields = [];

    ["name", "email", "timeline"].forEach((field) => {
      if (!formData.get(field)) {
        missingFields.push(field);
      }
    });

    if (missingFields.length) {
      if (statusNode) {
        statusNode.textContent = "Please complete the required fields before submitting.";
        statusNode.classList.remove("is-success");
        statusNode.classList.add("is-error");
      }
      return;
    }

    if (statusNode) {
      statusNode.textContent = "Thank you. I will reach out within two business days.";
      statusNode.classList.remove("is-error");
      statusNode.classList.add("is-success");
    }

    form.reset();
  });
}

function initialiseInsightsModal() {
  const modalContent = {
    "#modal-global": {
      title: "Global Launch Command",
      subtitle: "Executive Brief · Regulated Fintech",
      body: `
        <p>Built a 90-day mobilisation programme aligning legal, compliance, support, and partner operations across ten national entities. Established a real-time command centre with hourly readiness cadences and finalised an escalation playbook that reduced decision latency by 42%.</p>
        <ul>
          <li>Unified launch readiness scoring, audited weekly by regional leaders.</li>
          <li>Dedicated executive reporting suite with sentiment telemetry.</li>
          <li>Secured frictionless regulatory approvals ahead of target dates.</li>
        </ul>
      `,
    },
    "#modal-portfolio": {
      title: "Portfolio Governance Reset",
      subtitle: "Case Note · Enterprise SaaS",
      body: `
        <p>Partnered with finance and strategy to rationalise an overstretched portfolio. Introduced tiered investment guardrails, quarterly narrative reviews, and North-star metrics that connected capital deployment to business impact.</p>
        <ul>
          <li>Re-prioritised 18 initiatives into 3 investment horizons.</li>
          <li>Delivered artefacts for board storytelling and investor relations.</li>
          <li>Unlocked 11% operating margin lift without headcount reduction.</li>
        </ul>
      `,
    },
    "#modal-leadership": {
      title: "Leadership Residency",
      subtitle: "Memo · Product Organisation",
      body: `
        <p>Designed an immersive residency for rising product leaders focused on presence, influence, and executive composure. Participants produced refined narratives, stakeholder maps, and operating cadences tailored to complex organisations.</p>
        <ul>
          <li>12-week curriculum blending workshops, labs, and executive panels.</li>
          <li>Mentorship pairing with former C-suite mentors across industries.</li>
          <li>Post-programme adoption of calm-change frameworks across org.</li>
        </ul>
      `,
    },
  };

  const triggers = document.querySelectorAll("[data-modal-target]");
  if (!triggers.length) return;

  const modal = document.createElement("div");
  modal.className = "modal";
  modal.setAttribute("aria-hidden", "true");
  modal.innerHTML = `
    <div class="modal__overlay" data-modal-close tabindex="-1"></div>
    <div class="modal__dialog" role="dialog" aria-modal="true" aria-labelledby="modal-title" aria-describedby="modal-description" tabindex="-1">
      <button class="modal__close" type="button" data-modal-close aria-label="Close dialog">
        <span aria-hidden="true">&times;</span>
      </button>
      <div class="modal__content">
        <p class="modal__eyebrow" id="modal-eyebrow"></p>
        <h3 class="modal__title" id="modal-title"></h3>
        <div class="modal__body" id="modal-description"></div>
      </div>
    </div>
  `;

  document.body.append(modal);

  const overlay = modal.querySelector(".modal__overlay");
  const closeButtons = modal.querySelectorAll("[data-modal-close]");
  const titleNode = modal.querySelector("#modal-title");
  const eyebrowNode = modal.querySelector("#modal-eyebrow");
  const bodyNode = modal.querySelector("#modal-description");

  const closeModal = () => {
    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
    document.body.removeAttribute("data-modal-open");
  };

  const openModal = (targetId) => {
    const content = modalContent[targetId];
    if (!content) return;

    titleNode.textContent = content.title;
    eyebrowNode.textContent = content.subtitle;
    bodyNode.innerHTML = content.body;

    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");
    document.body.setAttribute("data-modal-open", "true");
    modal.querySelector(".modal__dialog").focus();
  };

  closeButtons.forEach((button) => button.addEventListener("click", closeModal));
  overlay?.addEventListener("click", closeModal);
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && modal.classList.contains("is-open")) {
      closeModal();
    }
  });

  triggers.forEach((trigger) =>
    trigger.addEventListener("click", () => {
      const target = trigger.dataset.modalTarget;
      if (target) {
        openModal(target);
      }
    })
  );
}

async function loadHeicImage() {
  const image = document.querySelector("[data-heic-src]");
  if (!image) return;

  const heicSource = image.dataset.heicSrc;
  if (!heicSource) return;

  try {
    const response = await fetch(heicSource);
    const blob = await response.blob();

    if (window.heic2any) {
      const convertedBlob = await window.heic2any({
        blob,
        toType: "image/jpeg",
        quality: 0.85,
      });
      const objectUrl = URL.createObjectURL(convertedBlob);
      image.src = objectUrl;
      image.addEventListener(
        "load",
        () => {
          URL.revokeObjectURL(objectUrl);
        },
        { once: true }
      );
    } else {
      image.src = heicSource;
    }
  } catch (error) {
    image.src = heicSource;
  }
}

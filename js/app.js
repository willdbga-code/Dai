/**
 * WILLIAM DEL BARRIO (PROZHE v1.1.0) FRONTEND ENGINE
 * 100% Driven by workout_program.json (window.WORKOUT_PROGRAM_DATA)
 */

(function () {
  'use strict';

  const DATA = window.WORKOUT_PROGRAM_DATA;
  if (!DATA) {
    console.error('WORKOUT_PROGRAM_DATA not found.');
    return;
  }

  // State Management
  const STATE = {
    heroSlideIndex: 0,
    heroInterval: null,
    scheduleFilter: 'all',
    activeExplorerDay: 1,
    activeRefCategory: 'all',
    restTimer: {
      remaining: 0,
      total: 0,
      label: 'Pronto para iniciar intervalo',
      intervalId: null,
      running: false
    },
    hydrationMl: parseInt(localStorage.getItem('dai_hydration_ml') || '1750', 10),
    nitricChecklist: JSON.parse(localStorage.getItem('dai_nitric_checks') || '[true, true, false, true]'),
    warmupChecks: JSON.parse(localStorage.getItem('dai_warmup_checks') || '{}'),
    workoutLogs: JSON.parse(localStorage.getItem('dai_workout_logs') || 'null'),
    weeklyMetrics: JSON.parse(localStorage.getItem('dai_weekly_metrics') || 'null'),
    formKneeRating: 5,
    formVascRating: 5
  };

  // Seed initial realistic progressive overload logs if empty
  const DEFAULT_LOGS = [
    {
      id: 'log-1',
      date: '2026-10-12',
      day_number: 1,
      exercise_id: 'Barbell Hip Thrust (Elevação Pélvica com Barra)',
      set_number: 1,
      weight_kg: 70,
      reps_performed: 10,
      actual_rir: '1',
      knee_comfort_rating_1_to_5: 5,
      vascularity_pump_rating_1_to_5: 4,
      notes: 'Contração isométrica de 1s no topo, tíbia 100% vertical, zero dor patelar.'
    },
    {
      id: 'log-2',
      date: '2026-10-13',
      day_number: 2,
      exercise_id: 'Superset Vascular de Braço (Rosca Inversa + Rosca Martelo)',
      set_number: 3,
      weight_kg: 10,
      reps_performed: 12,
      actual_rir: '1',
      knee_comfort_rating_1_to_5: 5,
      vascularity_pump_rating_1_to_5: 5,
      notes: 'Veia cefálica e rede dorsal do antebraço muito aparentes após sódio + beterraba pré-treino.'
    },
    {
      id: 'log-3',
      date: '2026-10-14',
      day_number: 3,
      exercise_id: 'Cadeira Flexora Sentada (Hamstring Stretch Superior)',
      set_number: 4,
      weight_kg: 45,
      reps_performed: 12,
      actual_rir: '0 (+6 Parciais)',
      knee_comfort_rating_1_to_5: 5,
      vascularity_pump_rating_1_to_5: 4,
      notes: 'Aplicadas 6 lengthened partials no alongamento máximo conforme Maeo et al. (2021).'
    },
    {
      id: 'log-4',
      date: '2026-10-16',
      day_number: 5,
      exercise_id: 'Kas Glute Bridge (no Smith ou com Barra)',
      set_number: 4,
      weight_kg: 75,
      reps_performed: 11,
      actual_rir: '1',
      knee_comfort_rating_1_to_5: 5,
      vascularity_pump_rating_1_to_5: 5,
      notes: '+5kg de sobrecarga progressiva no terço superior do movimento; tensão contínua.'
    }
  ];

  const DEFAULT_WEEKLY_METRICS = {
    body_weight_fasted_morning_average_kg: 62.4,
    glute_circumference_widest_cm: 98.5,
    mid_thigh_circumference_cm: 55.2,
    forearm_vascularity_visual_scale_1_to_5: 4,
    adherence_percentage: 100
  };

  if (!STATE.workoutLogs) {
    STATE.workoutLogs = DEFAULT_LOGS;
    localStorage.setItem('dai_workout_logs', JSON.stringify(STATE.workoutLogs));
  }
  if (!STATE.weeklyMetrics) {
    STATE.weeklyMetrics = DEFAULT_WEEKLY_METRICS;
    localStorage.setItem('dai_weekly_metrics', JSON.stringify(STATE.weeklyMetrics));
  }

  // Spectrum & Biomechanical 3D Card Metadata per Day (Prozhe spectrums + Blender 4.2 EEVEE Next 3D Renders)
  const DAY_CARD_META = {
    1: {
      category: 'lower',
      accentBg: 'linear-gradient(145deg, #252822 0%, #3d4337 52%, #181a17 100%)',
      badge: 'DIA 01 • SEGUNDA',
      shortCode: 'GLÚTEO H-VEC + QUAD',
      render3d: 'assets3d/day_1_3d.png',
      telemetryTop: 'VEC-01: HORIZONTAL PEAK (90° TIBIA)',
      telemetryBottom: '5 EXERCÍCIOS • 17 SÉRIES • KNEE-SAFE',
      spectrums: [
        {
          name: 'Vetor Dominante',
          label: 'Horizontal & Vertical',
          segments: ['Encurtado', 'Composto', 'Alongado'],
          active: [true, true, true]
        },
        {
          name: 'Tensão & RIR',
          label: 'RIR 1–2 [+Parciais]',
          segments: ['RIR 2', 'RIR 1', '+Parciais'],
          active: [true, true, true],
          vascular: true
        }
      ]
    },
    2: {
      category: 'upper',
      accentBg: 'linear-gradient(145deg, #2b1d23 0%, #442731 52%, #171316 100%)',
      badge: 'DIA 02 • TERÇA',
      shortCode: 'V-TAPER & VASCULAR A',
      render3d: 'assets3d/day_2_3d.png',
      telemetryTop: 'BRAQUIORRADIAL + DELTOIDE LATERAL 3D',
      telemetryBottom: '5 EXERCÍCIOS • 16 SÉRIES • SUPERSET',
      spectrums: [
        {
          name: 'Estímulo Vascular',
          label: 'Cefálica & Basílica',
          segments: ['Tração', 'Deltoide 3D', 'Pump VEGF'],
          active: [true, true, true],
          vascular: true
        },
        {
          name: 'Intensidade',
          label: 'RIR 0–2 [+Parciais]',
          segments: ['RIR 2', 'RIR 1', '+Parciais'],
          active: [true, true, true]
        }
      ]
    },
    3: {
      category: 'lower',
      accentBg: 'linear-gradient(145deg, #1f2922 0%, #37493c 55%, #141915 100%)',
      badge: 'DIA 03 • QUARTA',
      shortCode: 'GLÚTEO HINGE & ISQUIOS',
      render3d: 'assets3d/day_3_3d.png',
      telemetryTop: 'VEC-02: HIP HINGE & LENGTHENED TENSION',
      telemetryBottom: '4 EXERCÍCIOS • 15 SÉRIES • RDL + MAEO',
      spectrums: [
        {
          name: 'Curva de Resistência',
          label: 'Alongamento Extremo',
          segments: ['Hinge RDL', 'Flexora Sent.', 'Abdução 45°'],
          active: [true, true, true]
        },
        {
          name: 'Evidência Maeo 2021',
          label: '~2x Hipertrofia',
          segments: ['RIR 2', 'RIR 1', '+Parciais'],
          active: [true, true, true],
          vascular: true
        }
      ]
    },
    4: {
      category: 'upper',
      accentBg: 'linear-gradient(145deg, #27242c 0%, #3e3847 55%, #16141a 100%)',
      badge: 'DIA 04 • QUINTA',
      shortCode: 'SUPERIOR & FARMER WALK',
      render3d: 'assets3d/day_4_3d.png',
      telemetryTop: 'HIPEREMIA REATIVA • 40-50M FARMER WALK',
      telemetryBottom: '5 EXERCÍCIOS • 15 SÉRIES • PUMP VENOSO',
      spectrums: [
        {
          name: 'Foco Fisiológico',
          label: 'Oclusão + Hiperemia',
          segments: ['Clavicular', 'Escapular', 'Farmer Walk'],
          active: [true, true, true],
          vascular: true
        },
        {
          name: 'Dosagem RIR',
          label: 'RIR 1–2 Controlado',
          segments: ['Composto', 'Isolado', 'Isometria'],
          active: [true, true, true]
        }
      ]
    },
    5: {
      category: 'lower',
      accentBg: 'linear-gradient(145deg, #2d2124 0%, #4b3238 55%, #1a1416 100%)',
      badge: 'DIA 05 • SEXTA',
      shortCode: 'GLÚTEOS 3D & KAS BRIDGE',
      render3d: 'assets3d/day_5_3d.png',
      telemetryTop: 'VEC-03: 30° FRONTAL PLANE ABDUCTION',
      telemetryBottom: '5 EXERCÍCIOS • 17 SÉRIES • 3D GLUTE',
      spectrums: [
        {
          name: 'Síntese 3 Vetores',
          label: 'Kas + Déficit + Cabo 30°',
          segments: ['Horizontal', 'Unilateral', 'Abdução 30°'],
          active: [true, true, true]
        },
        {
          name: 'Densidade Final',
          label: 'RIR 0–2 Alta Tensão',
          segments: ['Tensão', 'Precisão', 'Metabólico'],
          active: [true, true, true],
          vascular: true
        }
      ]
    },
    6: {
      category: 'home',
      accentBg: 'linear-gradient(145deg, #292a22 0%, #484a3c 55%, #191a15 100%)',
      badge: 'DIA 06 • SÁBADO (CASA)',
      shortCode: 'HOME HYPER-PUMP (0 IMPACTO)',
      render3d: 'assets3d/day_6_3d.png',
      telemetryTop: 'METABOLIC SURGE • ZERO JOINT SHEAR',
      telemetryBottom: '5 EXERCÍCIOS • 14 SÉRIES • EM CASA',
      spectrums: [
        {
          name: 'Oclusão Metabólica',
          label: '15 a 30 Reps + Isometria',
          segments: ['Unilateral', 'Frog Pump', 'Hold 60s'],
          active: [true, true, true],
          vascular: true
        },
        {
          name: 'Estresse Articular',
          label: 'Zero Impacto Patelar',
          segments: ['RIR 0', 'Sem Carga', 'Capilar'],
          active: [true, true, true]
        }
      ]
    },
    7: {
      category: 'home',
      accentBg: 'linear-gradient(145deg, #1f2226 0%, #32383e 55%, #121417 100%)',
      badge: 'DIA 07 • DOMINGO',
      shortCode: 'SUPERCOMPENSAÇÃO & 3L+ ÁGUA',
      render3d: 'assets3d/day_7_3d.png',
      telemetryTop: 'SYSTEMIC RECOVERY & GLYCOGEN REFILL',
      telemetryBottom: 'DESCANSO TOTAL • REGENERAÇÃO ARTICULAR',
      spectrums: [
        {
          name: 'Fisiologia',
          label: 'Síntese Miofibrilar',
          segments: ['SNC Reset', 'Glicogênio', 'Hidratação'],
          active: [true, true, true]
        },
        {
          name: 'Recuperação Feminina',
          label: 'Laurent et al. (2010)',
          segments: ['Repouso', '124g Prot', '3.0L Água'],
          active: [true, true, true]
        }
      ]
    }
  };

  // =========================================================================
  // 1. NAVBAR DOCK, 4-DOT SUBMENU & SCROLL TRIGGER PILL
  // =========================================================================
  function initNavbarAndScrollTriggers() {
    const centerBar = document.getElementById('jn-center-bar');
    const dotsBtn = document.getElementById('jn-dots-toggle');

    if (dotsBtn && centerBar) {
      dotsBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        const isOpen = centerBar.classList.toggle('submenu-open');
        dotsBtn.setAttribute('aria-expanded', String(isOpen));
      });

      document.addEventListener('click', (e) => {
        if (!centerBar.contains(e.target)) {
          centerBar.classList.remove('submenu-open');
          dotsBtn.setAttribute('aria-expanded', 'false');
        }
      });

      centerBar.querySelectorAll('a[href^="#"]').forEach((link) => {
        link.addEventListener('click', () => {
          centerBar.classList.remove('submenu-open');
          dotsBtn.setAttribute('aria-expanded', 'false');
        });
      });
    }

    // Scroll threshold observer for floating selector pill
    const updateScrollState = () => {
      const scrollY = window.scrollY || document.documentElement.scrollTop;
      if (scrollY > 360) {
        document.body.classList.add('scrolled-past-hero');
      } else {
        document.body.classList.remove('scrolled-past-hero');
      }
    };
    window.addEventListener('scroll', updateScrollState, { passive: true });
    updateScrollState();
  }

  // =========================================================================
  // 2. HERO VIEWPORT CAROUSEL (3 SLIDES + FRACTION COUNTER)
  // =========================================================================
  function initHeroCarousel() {
    const slides = document.querySelectorAll('.hero-slide');
    const dots = document.querySelectorAll('.hero-slide-dot');
    const fractionEl = document.getElementById('hero-fraction-counter');
    if (!slides.length) return;

    function setSlide(index) {
      STATE.heroSlideIndex = (index + slides.length) % slides.length;
      slides.forEach((s, i) => {
        s.classList.toggle('active', i === STATE.heroSlideIndex);
      });
      dots.forEach((d, i) => {
        d.classList.toggle('active', i === STATE.heroSlideIndex);
      });
      if (fractionEl) {
        fractionEl.textContent = `${STATE.heroSlideIndex + 1} / ${slides.length}`;
      }
    }

    dots.forEach((dot, idx) => {
      dot.addEventListener('click', () => {
        setSlide(idx);
        resetAutoplay();
      });
    });

    function resetAutoplay() {
      if (STATE.heroInterval) clearInterval(STATE.heroInterval);
      STATE.heroInterval = setInterval(() => {
        setSlide(STATE.heroSlideIndex + 1);
      }, 6500);
    }

    resetAutoplay();
  }

  // =========================================================================
  // 3. 3D HOLOGRAPHIC CARD ENGINE (Prozhe theme.js math)
  // =========================================================================
  function bindHoloCardEvents(root = document) {
    const holoCards = root.querySelectorAll('.card-holo');
    holoCards.forEach((card) => {
      if (card.dataset.holoBound === 'true') return;
      card.dataset.holoBound = 'true';

      card.addEventListener('mousemove', (s) => {
        const rect = card.getBoundingClientRect();
        const e = (s.clientX - rect.left) / (card.clientWidth || 1);
        const i = (s.clientY - rect.top) / (card.clientHeight || 1);
        const r = -(e - 0.5) * 6;
        const n = (i - 0.5) * 6;
        const o = 40 + 20 * e;
        const a = 40 + 20 * i;

        card.style.setProperty('--x', `${(100 * e).toFixed(1)}%`);
        card.style.setProperty('--y', `${(100 * i).toFixed(1)}%`);
        card.style.setProperty('--bg-x', `${o.toFixed(1)}%`);
        card.style.setProperty('--bg-y', `${a.toFixed(1)}%`);
        card.style.setProperty('--r-x', `${r.toFixed(2)}deg`);
        card.style.setProperty('--r-y', `${n.toFixed(2)}deg`);
        card.style.setProperty('--s', '1.015');
      });

      card.addEventListener('mouseleave', () => {
        card.style.setProperty('--x', '50%');
        card.style.setProperty('--y', '50%');
        card.style.setProperty('--bg-x', '50%');
        card.style.setProperty('--bg-y', '50%');
        card.style.setProperty('--r-x', '0deg');
        card.style.setProperty('--r-y', '0deg');
        card.style.setProperty('--s', '1');
      });
    });
  }

  // =========================================================================
  // 4. RENDER 7 HOLOGRAPHIC SCHEDULE CARDS (.card-holo + spectrums)
  // =========================================================================
  function renderScheduleHoloCards() {
    const grid = document.getElementById('schedule-holo-grid');
    if (!grid) return;

    const filteredDays = DATA.schedule.filter((day) => {
      if (STATE.scheduleFilter === 'all') return true;
      const meta = DAY_CARD_META[day.day_number];
      return meta && meta.category === STATE.scheduleFilter;
    });

    grid.innerHTML = filteredDays
      .map((day) => {
        const meta = DAY_CARD_META[day.day_number];
        const totalSets = day.exercises.reduce((acc, ex) => acc + (ex.sets || 0), 0);
        const hasPartials = day.exercises.some((ex) => ex.has_lengthened_partials);

        const spectrumHtml = meta.spectrums
          .map(
            (spec) => `
          <div class="spectrum-box">
            <div class="spectrum-header">
              <span class="spectrum-name">${spec.name}:</span>
              <span class="spectrum-pill">${spec.label}</span>
            </div>
            <div class="spectrum-segments" role="meter" aria-label="${spec.name}: ${spec.label}">
              ${spec.segments
                .map(
                  (seg, idx) => `
                <div class="spectrum-segment-col">
                  <span class="spectrum-bar ${
                    spec.active[idx] ? (spec.vascular ? 'active-vascular' : 'active') : ''
                  }"></span>
                  <div class="spectrum-seg-label">
                    <span>${seg}</span>
                    ${
                      spec.active[idx]
                        ? `<svg width="10" height="10" viewBox="0 0 512 512" fill="currentColor"><path d="M186.301 339.893L96 249.461l-32 30.507L186.301 402 448 140.506 416 110z"/></svg>`
                        : ''
                    }
                  </div>
                </div>
              `
                )
                .join('')}
            </div>
          </div>
        `
          )
          .join('');

        return `
        <article class="product-card" data-day="${day.day_number}">
          <div class="card-holo" role="button" tabindex="0" aria-label="Abrir detalhes de ${day.day_name}: ${day.session_name}" data-open-day="${day.day_number}">
            <div class="card-transform" style="background: ${meta.accentBg};">
              <div class="card-badge-tl">
                <span class="micro-badge">${meta.badge}</span>
                ${hasPartials ? `<span class="micro-badge micro-badge-vascular">+PARCIAIS</span>` : ''}
              </div>

              <div style="width:100%;height:100%;display:flex;flex-direction:column;justify-content:space-between;padding:48px 16px 52px;position:relative;z-index:10;">
                <span class="caption-sm" style="color:rgba(255,255,255,0.68);letter-spacing:0.06em;font-size:0.6rem;">${meta.telemetryTop}</span>
                <div style="flex:1;display:flex;align-items:center;justify-content:center;min-height:0;padding:4px 0;">
                  <img src="${meta.render3d}" alt="${day.day_name} — ${day.session_name}" style="width:92%;height:92%;object-fit:contain;filter:drop-shadow(0 18px 26px rgba(0,0,0,0.62));transition:transform 0.35s cubic-bezier(0,0.4,0,1.02);" />
                </div>
                <span class="caption-sm" style="color:rgba(255,255,255,0.88);letter-spacing:0.05em;font-size:0.62rem;">${meta.telemetryBottom}</span>
              </div>

              <div class="card-spotlight"></div>
              <div class="card-holo-overlay"></div>

              <div class="card-quickview-br">
                <span class="card-QuickPlus">
                  <svg viewBox="0 0 32 32" width="14" height="14" fill="currentColor">
                    <path d="M 15 5 L 15 15 L 5 15 L 5 17 L 15 17 L 15 27 L 17 27 L 17 17 L 27 17 L 27 15 L 17 15 L 17 5 Z"/>
                  </svg>
                </span>
                <span>Inspecionar Dia</span>
              </div>
            </div>
          </div>

          <div class="card-info-stack">
            <div class="card-title-row">
              <h4 class="card-title">${day.day_name} — ${day.session_name}</h4>
              <div class="card-meta-line">
                <span>${day.location}</span>
                <span>★ ${day.exercises.length} Ex • ${totalSets} Séries</span>
              </div>
            </div>
            ${spectrumHtml}
          </div>
        </article>
      `;
      })
      .join('');

    bindHoloCardEvents(grid);

    // Bind click & keyboard events to open Quick View Modal & sync Explorer
    grid.querySelectorAll('[data-open-day]').forEach((el) => {
      const handleActivate = () => {
        const dayNum = parseInt(el.getAttribute('data-open-day'), 10);
        STATE.activeExplorerDay = dayNum;
        renderMasterExplorer();
        openDayQuickViewModal(dayNum);
      };
      el.addEventListener('click', handleActivate);
      el.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          handleActivate();
        }
      });
    });
  }

  function initScheduleFilters() {
    const filterBtns = document.querySelectorAll('[data-schedule-filter]');
    filterBtns.forEach((btn) => {
      btn.addEventListener('click', () => {
        STATE.scheduleFilter = btn.getAttribute('data-schedule-filter');
        filterBtns.forEach((b) => b.classList.toggle('active', b === btn));
        renderScheduleHoloCards();
      });
    });
  }

  // =========================================================================
  // 5. INTERACTIVE MASTER WORKOUT EXPLORER & LIVE REST TIMER
  // =========================================================================
  function renderMasterExplorer() {
    const strip = document.getElementById('explorer-day-strip');
    const body = document.getElementById('explorer-day-body');
    if (!strip || !body) return;

    strip.innerHTML = DATA.schedule
      .map((day) => {
        const isActive = day.day_number === STATE.activeExplorerDay;
        const totalSets = day.exercises.reduce((a, b) => a + (b.sets || 0), 0);
        return `
        <button type="button" class="day-tab-btn ${isActive ? 'active' : ''}" data-select-day="${day.day_number}">
          <span class="caption-sm" style="opacity:0.72;">DIA 0${day.day_number} • ${day.day_name.slice(0, 3).toUpperCase()}</span>
          <span style="font-weight:600;font-size:0.84rem;line-height:1.2;">${day.session_name.split('(')[0].trim()}</span>
          <span class="caption-sm" style="opacity:0.65;margin-top:2px;">${day.exercises.length ? `${day.exercises.length} Ex • ${totalSets} Séries` : 'Recuperação'}</span>
        </button>
      `;
      })
      .join('');

    strip.querySelectorAll('[data-select-day]').forEach((btn) => {
      btn.addEventListener('click', () => {
        STATE.activeExplorerDay = parseInt(btn.getAttribute('data-select-day'), 10);
        renderMasterExplorer();
      });
    });

    const dayData = DATA.schedule.find((d) => d.day_number === STATE.activeExplorerDay) || DATA.schedule[0];
    const dayChecks = STATE.warmupChecks[dayData.day_number] || [];

    const warmupHtml =
      dayData.warmup && dayData.warmup.length
        ? `
      <div class="warmup-banner">
        <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap;">
          <span class="caption" style="font-weight:700;">PROTOCOLO DE AQUECIMENTO & PREPARAÇÃO SINOVIAL (${dayData.day_name.toUpperCase()})</span>
          <span class="caption-sm">Marque ao concluir antes da 1ª série de trabalho</span>
        </div>
        <div class="warmup-list">
          ${dayData.warmup
            .map(
              (w, idx) => `
            <label class="warmup-chip">
              <input type="checkbox" data-warmup-day="${dayData.day_number}" data-warmup-idx="${idx}" ${
                dayChecks.includes(idx) ? 'checked' : ''
              }>
              <span>${w}</span>
            </label>
          `
            )
            .join('')}
        </div>
      </div>
    `
        : '';

    const exercisesHtml =
      dayData.exercises && dayData.exercises.length
        ? `
      <div class="exercise-table-wrap">
        <table class="jn-table">
          <thead>
            <tr>
              <th style="width:44px;">#</th>
              <th>EXERCÍCIO, MÚSCULOS-ALVO & VETOR</th>
              <th style="width:76px;text-align:center;">SÉRIES</th>
              <th style="width:110px;text-align:center;">REPS</th>
              <th style="width:84px;text-align:center;">RIR</th>
              <th style="width:118px;text-align:center;">DESCANSO</th>
              <th>NOTAS BIOMECÂNICAS & EXECUÇÃO</th>
              <th style="width:115px;text-align:center;">AÇÃO</th>
            </tr>
          </thead>
          <tbody>
            ${dayData.exercises
              .map(
                (ex) => `
              <tr>
                <td style="text-align:center;font-family:var(--font-mono);font-weight:700;">0${ex.order}</td>
                <td>
                  <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">
                    <strong style="font-size:0.93rem;">${ex.name}</strong>
                    ${
                      ex.has_lengthened_partials
                        ? `<span class="micro-badge micro-badge-vascular" title="Na última série, realizar 5-6 repetições parciais no ponto de máximo alongamento">[+Lengthened Partials]</span>`
                        : ''
                    }
                  </div>
                  <div class="caption-sm" style="color:rgba(28,28,28,0.72);margin-top:4px;">
                    VETOR: ${ex.vector} • ALVO: ${ex.target_muscles.join(', ')}
                  </div>
                </td>
                <td style="text-align:center;font-family:var(--font-mono);font-weight:700;font-size:0.95rem;">${ex.sets}</td>
                <td style="text-align:center;font-family:var(--font-mono);">${ex.reps}</td>
                <td style="text-align:center;font-family:var(--font-mono);font-weight:600;">${ex.rir}</td>
                <td style="text-align:center;">
                  <button type="button" class="btn-pill btn-pill-dark" style="padding:5px 10px;font-size:0.68rem;" data-start-rest="${ex.rest_seconds}" data-rest-ex="${ex.name}">
                    ⏱ ${ex.rest_seconds}s
                  </button>
                </td>
                <td style="font-size:0.83rem;line-height:1.45;color:rgba(28,28,28,0.88);">${ex.notes}</td>
                <td style="text-align:center;">
                  <button type="button" class="btn-pill btn-pill-outline" style="padding:6px 11px;font-size:0.65rem;" data-prefill-log-day="${dayData.day_number}" data-prefill-log-ex="${ex.name}">
                    + Logar Série
                  </button>
                </td>
              </tr>
            `
              )
              .join('')}
          </tbody>
        </table>
      </div>
    `
        : `
      <div class="jn-surface-card" style="background:rgba(255,255,255,0.48);padding:28px;text-align:center;align-items:center;">
        <span class="micro-badge micro-badge-dark">DIA 07 • DOMINGO DE SUPERCOMPENSAÇÃO</span>
        <h4 class="h3" style="margin-top:6px;">${dayData.session_name}</h4>
        <p class="paragraph" style="max-width:60ch;color:rgba(28,28,28,0.8);">
          ${dayData.target_focus}. Mantenha a ingestão de <strong>124g de proteínas</strong>, <strong>260–300g de carboidratos</strong> e <strong>2,5L a 3,0L de água</strong> para maximizar a ressíntese de glicogênio intramuscular e remodelação miofibrilar.
        </p>
      </div>
    `;

    body.innerHTML = `
      <div style="display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:14px;">
        <div>
          <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px;">
            <span class="micro-badge micro-badge-dark">DIA 0${dayData.day_number} • ${dayData.day_name.toUpperCase()}</span>
            <span class="micro-badge">${dayData.location}</span>
          </div>
          <h3 class="h3">${dayData.session_name}</h3>
          <p class="paragraph" style="color:rgba(28,28,28,0.75);margin-top:2px;">Foco Biomecânico: ${dayData.target_focus}</p>
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;">
          <button type="button" class="btn-pill btn-pill-dark" id="btn-open-modal-from-explorer" data-day="${dayData.day_number}">
            Modo Ficha Tela Cheia
          </button>
          <a href="Treino_Hipertrofia_Feminina_WilliamDelBarrio.pdf" download class="btn-pill btn-pill-outline">
            Baixar PDF Oficial
          </a>
        </div>
      </div>
      ${warmupHtml}
      ${exercisesHtml}
    `;

    // Bind warmup checkboxes
    body.querySelectorAll('[data-warmup-day]').forEach((cb) => {
      cb.addEventListener('change', () => {
        const dNum = parseInt(cb.getAttribute('data-warmup-day'), 10);
        const wIdx = parseInt(cb.getAttribute('data-warmup-idx'), 10);
        const arr = new Set(STATE.warmupChecks[dNum] || []);
        if (cb.checked) arr.add(wIdx);
        else arr.delete(wIdx);
        STATE.warmupChecks[dNum] = Array.from(arr);
        localStorage.setItem('dai_warmup_checks', JSON.stringify(STATE.warmupChecks));
      });
    });

    // Bind rest timer buttons
    body.querySelectorAll('[data-start-rest]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const sec = parseInt(btn.getAttribute('data-start-rest'), 10);
        const exName = btn.getAttribute('data-rest-ex');
        startRestCountdown(sec, exName);
      });
    });

    // Bind prefill log buttons
    body.querySelectorAll('[data-prefill-log-ex]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const dNum = parseInt(btn.getAttribute('data-prefill-log-day'), 10);
        const exName = btn.getAttribute('data-prefill-log-ex');
        prefillLogForm(dNum, exName);
      });
    });

    const modalBtn = document.getElementById('btn-open-modal-from-explorer');
    if (modalBtn) {
      modalBtn.addEventListener('click', () => openDayQuickViewModal(dayData.day_number));
    }
  }

  // Live Rest Countdown Timer (Schoenfeld et al., 2016: 90s - 150s)
  function startRestCountdown(seconds, exerciseLabel) {
    if (STATE.restTimer.intervalId) {
      clearInterval(STATE.restTimer.intervalId);
    }
    STATE.restTimer.total = seconds;
    STATE.restTimer.remaining = seconds;
    STATE.restTimer.label = exerciseLabel || `Intervalo Científico (${seconds}s)`;
    STATE.restTimer.running = true;
    updateRestTimerUI();

    STATE.restTimer.intervalId = setInterval(() => {
      if (STATE.restTimer.remaining > 0) {
        STATE.restTimer.remaining -= 1;
        updateRestTimerUI();
      } else {
        clearInterval(STATE.restTimer.intervalId);
        STATE.restTimer.running = false;
        STATE.restTimer.label = `✓ Descanso concluído! Pronta para a próxima série (${exerciseLabel || ''})`;
        updateRestTimerUI();
      }
    }, 1000);
  }

  function updateRestTimerUI() {
    const timeEl = document.getElementById('rest-timer-clock');
    const labelEl = document.getElementById('rest-timer-label');
    const fillEl = document.getElementById('rest-timer-progress');
    if (!timeEl || !labelEl) return;

    const mins = Math.floor(STATE.restTimer.remaining / 60);
    const secs = STATE.restTimer.remaining % 60;
    timeEl.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    labelEl.textContent = STATE.restTimer.label;

    if (fillEl) {
      const pct = STATE.restTimer.total > 0 ? ((STATE.restTimer.total - STATE.restTimer.remaining) / STATE.restTimer.total) * 100 : 0;
      fillEl.style.width = `${pct}%`;
    }
  }

  function initRestTimerControls() {
    document.querySelectorAll('[data-preset-timer]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const sec = parseInt(btn.getAttribute('data-preset-timer'), 10);
        const label = btn.getAttribute('data-preset-label');
        startRestCountdown(sec, label);
      });
    });

    const resetBtn = document.getElementById('rest-timer-reset');
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        if (STATE.restTimer.intervalId) clearInterval(STATE.restTimer.intervalId);
        STATE.restTimer.remaining = 0;
        STATE.restTimer.total = 0;
        STATE.restTimer.running = false;
        STATE.restTimer.label = 'Timer zerado. Clique no descanso de qualquer exercício.';
        updateRestTimerUI();
      });
    }
  }

  // =========================================================================
  // 6. SLIDE-OVER QUICK VIEW MODAL (my-modal architecture)
  // =========================================================================
  function openDayQuickViewModal(dayNum) {
    const backdrop = document.getElementById('day-quickview-modal');
    const titleEl = document.getElementById('modal-day-title');
    const bodyEl = document.getElementById('modal-day-body');
    if (!backdrop || !titleEl || !bodyEl) return;

    const dayData = DATA.schedule.find((d) => d.day_number === dayNum);
    if (!dayData) return;

    titleEl.textContent = `DIA 0${dayData.day_number}: ${dayData.day_name.toUpperCase()}`;

    bodyEl.innerHTML = `
      <div style="display:flex;flex-direction:column;gap:8px;">
        <div style="display:flex;gap:6px;flex-wrap:wrap;">
          <span class="micro-badge micro-badge-dark">${dayData.location}</span>
          <span class="micro-badge">${dayData.exercises.length} Exercícios Prescritos</span>
        </div>
        <h3 class="h3">${dayData.session_name}</h3>
        <p class="paragraph" style="color:rgba(28,28,28,0.8);">${dayData.target_focus}</p>
      </div>

      ${
        dayData.warmup && dayData.warmup.length
          ? `
        <div class="jn-surface-card" style="background:rgba(255,255,255,0.5);">
          <span class="caption" style="font-weight:700;">AQUECIMENTO ESPECÍFICO DA SESSÃO</span>
          <ul style="padding-left:18px;display:flex;flex-direction:column;gap:4px;font-size:0.88rem;">
            ${dayData.warmup.map((w) => `<li>${w}</li>`).join('')}
          </ul>
        </div>
      `
          : ''
      }

      <div style="display:flex;flex-direction:column;gap:12px;">
        ${
          dayData.exercises.length
            ? dayData.exercises
                .map(
                  (ex) => `
          <div class="jn-surface-card" style="background:rgba(255,255,255,0.65);">
            <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:10px;flex-wrap:wrap;">
              <div>
                <span class="caption-sm" style="color:rgba(28,28,28,0.65);">EXERCÍCIO 0${ex.order} • ${ex.vector}</span>
                <h4 style="font-size:1.02rem;font-weight:700;margin-top:2px;">${ex.name}</h4>
              </div>
              ${
                ex.has_lengthened_partials
                  ? `<span class="micro-badge micro-badge-vascular">+5-6 LENGTHENED PARTIALS NA ÚLTIMA SÉRIE</span>`
                  : ''
              }
            </div>
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;background:rgba(28,28,28,0.08);padding:10px;border-radius:6px;font-family:var(--font-mono);font-size:0.75rem;">
              <div><span style="opacity:0.6;display:block;font-size:0.62rem;">SÉRIES</span><strong>${ex.sets}</strong></div>
              <div><span style="opacity:0.6;display:block;font-size:0.62rem;">REPS</span><strong>${ex.reps}</strong></div>
              <div><span style="opacity:0.6;display:block;font-size:0.62rem;">RIR</span><strong>${ex.rir}</strong></div>
              <div><span style="opacity:0.6;display:block;font-size:0.62rem;">DESCANSO</span><strong>${ex.rest_seconds}s</strong></div>
            </div>
            <p style="font-size:0.85rem;color:rgba(28,28,28,0.88);">${ex.notes}</p>
            <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap;padding-top:4px;">
              <span class="caption-sm">Músculos: ${ex.target_muscles.join(', ')}</span>
              <button type="button" class="btn-pill btn-pill-dark" style="padding:6px 14px;font-size:0.68rem;" data-modal-log-day="${dayData.day_number}" data-modal-log-ex="${ex.name}">
                Registrar Série no Log
              </button>
            </div>
          </div>
        `
                )
                .join('')
            : `<p class="paragraph">Domingo dedicado à Supercompensação Sistêmica & Recuperação Miofibrilar.</p>`
        }
      </div>
    `;

    bodyEl.querySelectorAll('[data-modal-log-ex]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const dNum = parseInt(btn.getAttribute('data-modal-log-day'), 10);
        const exName = btn.getAttribute('data-modal-log-ex');
        closeModals();
        prefillLogForm(dNum, exName);
      });
    });

    backdrop.classList.add('open');
    document.body.classList.add('modal-open');
  }

  function closeModals() {
    document.querySelectorAll('.jn-modal-backdrop').forEach((m) => m.classList.remove('open'));
    document.body.classList.remove('modal-open');
  }

  function initModals() {
    document.querySelectorAll('[data-close-modal]').forEach((btn) => {
      btn.addEventListener('click', closeModals);
    });
    document.querySelectorAll('.jn-modal-backdrop').forEach((backdrop) => {
      backdrop.addEventListener('click', (e) => {
        if (e.target === backdrop) closeModals();
      });
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeModals();
    });
  }

  // =========================================================================
  // 7. SCIENTIFIC PILLARS, NITRIC OXIDE HYDRATION & PUBMED REFERENCES
  // =========================================================================
  function renderScientificPillars() {
    const container = document.getElementById('scientific-pillars-grid');
    if (!container) return;

    container.innerHTML = DATA.scientific_pillars
      .map(
        (p, idx) => `
      <div class="jn-surface-card">
        <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;">
          <span class="micro-badge micro-badge-dark">PILAR 0${idx + 1}</span>
          <span class="caption-sm" style="color:rgba(28,28,28,0.72);">${p.reference}</span>
        </div>
        <h4 class="h4">${p.pillar}</h4>
        <p class="paragraph" style="font-size:0.88rem;color:rgba(28,28,28,0.82);">${p.application}</p>
      </div>
    `
      )
      .join('');
  }

  function renderNitricOxideAndHydration() {
    const listEl = document.getElementById('nitric-oxide-protocol-list');
    const waterValEl = document.getElementById('hydration-current-val');
    const waterBarEl = document.getElementById('hydration-progress-bar');

    if (listEl) {
      listEl.innerHTML = DATA.nutrition_and_vascularity_guidelines.vascularity_nitric_oxide_protocol
        .map((item, idx) => {
          const parts = item.split(':');
          const title = parts[0];
          const rest = parts.slice(1).join(':');
          const checked = STATE.nitricChecklist[idx] ? 'checked' : '';
          return `
          <label class="jn-surface-card" style="cursor:pointer;flex-direction:row;align-items:flex-start;gap:12px;">
            <input type="checkbox" data-nitric-idx="${idx}" ${checked} style="margin-top:4px;width:16px;height:16px;accent-color:hsl(var(--color-vascular));flex-shrink:0;">
            <div>
              <strong style="font-size:0.92rem;display:block;margin-bottom:3px;">${title}</strong>
              <span style="font-size:0.85rem;color:rgba(28,28,28,0.8);">${rest}</span>
            </div>
          </label>
        `;
        })
        .join('');

      listEl.querySelectorAll('[data-nitric-idx]').forEach((cb) => {
        cb.addEventListener('change', () => {
          const i = parseInt(cb.getAttribute('data-nitric-idx'), 10);
          STATE.nitricChecklist[i] = cb.checked;
          localStorage.setItem('dai_nitric_checks', JSON.stringify(STATE.nitricChecklist));
        });
      });
    }

    function updateHydrationUI() {
      const targetMl = 2800; // 45ml/kg * 62kg
      if (waterValEl) waterValEl.textContent = `${STATE.hydrationMl} / ${targetMl} ml`;
      if (waterBarEl) {
        const pct = Math.min(100, Math.round((STATE.hydrationMl / targetMl) * 100));
        waterBarEl.style.width = `${pct}%`;
      }
    }

    document.querySelectorAll('[data-add-water]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const delta = parseInt(btn.getAttribute('data-add-water'), 10);
        if (delta === 0) STATE.hydrationMl = 0;
        else STATE.hydrationMl = Math.max(0, Math.min(4500, STATE.hydrationMl + delta));
        localStorage.setItem('dai_hydration_ml', String(STATE.hydrationMl));
        updateHydrationUI();
      });
    });

    updateHydrationUI();
  }

  // =========================================================================
  // 8. CONSTANCY LOGSHEET & PROGRESSIVE OVERLOAD TRACKER
  // =========================================================================
  function initConstancyTracker() {
    const daySelect = document.getElementById('log-day-select');
    const exSelect = document.getElementById('log-exercise-select');
    const dateInput = document.getElementById('log-date-input');
    const form = document.getElementById('workout-log-form');

    if (dateInput && !dateInput.value) {
      dateInput.value = new Date().toISOString().split('T')[0];
    }

    if (daySelect && exSelect) {
      const gymDays = DATA.schedule.filter((d) => d.exercises && d.exercises.length > 0);
      daySelect.innerHTML = gymDays
        .map((d) => `<option value="${d.day_number}">Dia 0${d.day_number} — ${d.day_name} (${d.session_name.split('(')[0].trim()})</option>`)
        .join('');

      const populateExercisesForDay = (dNum) => {
        const dayObj = DATA.schedule.find((d) => d.day_number === Number(dNum)) || gymDays[0];
        exSelect.innerHTML = dayObj.exercises
          .map((ex) => `<option value="${ex.name}">${ex.order}. ${ex.name} (${ex.sets}x ${ex.reps})</option>`)
          .join('');
      };

      populateExercisesForDay(daySelect.value);
      daySelect.addEventListener('change', () => populateExercisesForDay(daySelect.value));
    }

    // Rating Pill Selectors (1 to 5)
    document.querySelectorAll('[data-knee-rating]').forEach((btn) => {
      btn.addEventListener('click', () => {
        STATE.formKneeRating = parseInt(btn.getAttribute('data-knee-rating'), 10);
        document.querySelectorAll('[data-knee-rating]').forEach((b) => b.classList.toggle('active', b === btn));
      });
    });

    document.querySelectorAll('[data-vasc-rating]').forEach((btn) => {
      btn.addEventListener('click', () => {
        STATE.formVascRating = parseInt(btn.getAttribute('data-vasc-rating'), 10);
        document.querySelectorAll('[data-vasc-rating]').forEach((b) => b.classList.toggle('active', b === btn));
      });
    });

    if (form) {
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        const newEntry = {
          id: 'log-' + Date.now(),
          date: document.getElementById('log-date-input').value || '2026-10-16',
          day_number: parseInt(document.getElementById('log-day-select').value, 10),
          exercise_id: document.getElementById('log-exercise-select').value,
          set_number: parseInt(document.getElementById('log-set-input').value || '1', 10),
          weight_kg: parseFloat(document.getElementById('log-weight-input').value || '0'),
          reps_performed: parseInt(document.getElementById('log-reps-input').value || '10', 10),
          actual_rir: document.getElementById('log-rir-input').value || '1',
          knee_comfort_rating_1_to_5: STATE.formKneeRating,
          vascularity_pump_rating_1_to_5: STATE.formVascRating,
          notes: document.getElementById('log-notes-input').value.trim() || 'Execução técnica controlada dentro da meta RIR.'
        };

        STATE.workoutLogs.unshift(newEntry);
        localStorage.setItem('dai_workout_logs', JSON.stringify(STATE.workoutLogs));
        renderWorkoutLogsTable();
        document.getElementById('log-notes-input').value = '';
      });
    }

    // Weekly Progress Indicators Form
    const weeklyForm = document.getElementById('weekly-metrics-form');
    if (weeklyForm) {
      const m = STATE.weeklyMetrics;
      document.getElementById('wm-weight').value = m.body_weight_fasted_morning_average_kg;
      document.getElementById('wm-glute').value = m.glute_circumference_widest_cm;
      document.getElementById('wm-thigh').value = m.mid_thigh_circumference_cm;
      document.getElementById('wm-vasc').value = m.forearm_vascularity_visual_scale_1_to_5;
      document.getElementById('wm-adherence').value = m.adherence_percentage;

      weeklyForm.addEventListener('submit', (e) => {
        e.preventDefault();
        STATE.weeklyMetrics = {
          body_weight_fasted_morning_average_kg: parseFloat(document.getElementById('wm-weight').value || '62'),
          glute_circumference_widest_cm: parseFloat(document.getElementById('wm-glute').value || '98.5'),
          mid_thigh_circumference_cm: parseFloat(document.getElementById('wm-thigh').value || '55'),
          forearm_vascularity_visual_scale_1_to_5: parseInt(document.getElementById('wm-vasc').value || '4', 10),
          adherence_percentage: parseInt(document.getElementById('wm-adherence').value || '100', 10)
        };
        localStorage.setItem('dai_weekly_metrics', JSON.stringify(STATE.weeklyMetrics));
        renderWeeklyMetricsSummary();
      });
    }

    // Export JSON button
    const exportBtn = document.getElementById('btn-export-logs');
    if (exportBtn) {
      exportBtn.addEventListener('click', () => {
        const payload = {
          athlete: DATA.program_metadata.target_athlete,
          weekly_progress_indicators: STATE.weeklyMetrics,
          workout_logs: STATE.workoutLogs
        };
        const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `constancia_dai_williamdelbarrio_${new Date().toISOString().slice(0, 10)}.json`;
        a.click();
        URL.revokeObjectURL(url);
      });
    }

    renderWorkoutLogsTable();
    renderWeeklyMetricsSummary();
  }

  function prefillLogForm(dayNum, exerciseName) {
    const daySelect = document.getElementById('log-day-select');
    const exSelect = document.getElementById('log-exercise-select');
    if (daySelect && exSelect) {
      daySelect.value = String(dayNum);
      daySelect.dispatchEvent(new Event('change'));
      exSelect.value = exerciseName;
    }
    const section = document.getElementById('constancia-tracker');
    if (section) {
      section.scrollIntoView({ behavior: 'smooth' });
      setTimeout(() => {
        const wInput = document.getElementById('log-weight-input');
        if (wInput) wInput.focus();
      }, 450);
    }
  }

  function renderWorkoutLogsTable() {
    const tbody = document.getElementById('workout-logs-tbody');
    const badgeCount = document.getElementById('nav-log-count');
    if (badgeCount) badgeCount.textContent = String(STATE.workoutLogs.length);
    if (!tbody) return;

    tbody.innerHTML = STATE.workoutLogs
      .map(
        (log) => `
      <tr>
        <td style="font-family:var(--font-mono);font-size:0.78rem;white-space:nowrap;">${log.date}<br/><span style="opacity:0.6;">Dia 0${log.day_number}</span></td>
        <td>
          <strong>${log.exercise_id}</strong>
          <div style="font-size:0.78rem;color:rgba(28,28,28,0.72);margin-top:2px;">${log.notes}</div>
        </td>
        <td style="text-align:center;font-family:var(--font-mono);">#${log.set_number}</td>
        <td style="text-align:center;font-family:var(--font-mono);font-weight:700;">${log.weight_kg} kg</td>
        <td style="text-align:center;font-family:var(--font-mono);">${log.reps_performed}</td>
        <td style="text-align:center;font-family:var(--font-mono);">${log.actual_rir}</td>
        <td style="text-align:center;font-family:var(--font-mono);">${log.knee_comfort_rating_1_to_5}/5</td>
        <td style="text-align:center;font-family:var(--font-mono);color:hsl(var(--color-vascular));font-weight:700;">${log.vascularity_pump_rating_1_to_5}/5</td>
        <td style="text-align:center;">
          <button type="button" class="filter-pill" data-delete-log="${log.id}" title="Remover registro">✕</button>
        </td>
      </tr>
    `
      )
      .join('');

    tbody.querySelectorAll('[data-delete-log]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const id = btn.getAttribute('data-delete-log');
        STATE.workoutLogs = STATE.workoutLogs.filter((l) => l.id !== id);
        localStorage.setItem('dai_workout_logs', JSON.stringify(STATE.workoutLogs));
        renderWorkoutLogsTable();
      });
    });
  }

  function renderWeeklyMetricsSummary() {
    const strip = document.getElementById('weekly-kpi-strip');
    if (!strip) return;
    const m = STATE.weeklyMetrics;
    strip.innerHTML = `
      <div class="jn-surface-card" style="padding:12px 14px;">
        <span class="caption-sm">PESO EM JEJUM (MÉDIA)</span>
        <strong class="h3 tabular-nums">${m.body_weight_fasted_morning_average_kg} kg</strong>
        <span class="caption-sm" style="opacity:0.65;">Base: 62,0 kg (+0,8 a 1,2kg/mês)</span>
      </div>
      <div class="jn-surface-card" style="padding:12px 14px;">
        <span class="caption-sm">CIRCUNFERÊNCIA GLÚTEO</span>
        <strong class="h3 tabular-nums">${m.glute_circumference_widest_cm} cm</strong>
        <span class="caption-sm" style="opacity:0.65;">Ponto de maior projeção 3D</span>
      </div>
      <div class="jn-surface-card" style="padding:12px 14px;">
        <span class="caption-sm">COXA MÉDIA</span>
        <strong class="h3 tabular-nums">${m.mid_thigh_circumference_cm} cm</strong>
        <span class="caption-sm" style="opacity:0.65;">Vasto Lateral + Isquiotibiais</span>
      </div>
      <div class="jn-surface-card" style="padding:12px 14px;">
        <span class="caption-sm">ESCALA VASCULAR ANTEBRAÇO</span>
        <strong class="h3 tabular-nums" style="color:hsl(var(--color-vascular));">${m.forearm_vascularity_visual_scale_1_to_5} / 5</strong>
        <span class="caption-sm" style="opacity:0.65;">Aderência Semanal: ${m.adherence_percentage}%</span>
      </div>
    `;
  }

  // =========================================================================
  // 9. PUBMED BIBLIOGRAPHIC REFERENCES & 7-PAGE PDF PREVIEWER
  // =========================================================================
  function initReferencesAndPdfPreview() {
    const filterContainer = document.getElementById('ref-category-filters');
    const gridContainer = document.getElementById('references-list-grid');
    if (!filterContainer || !gridContainer) return;

    const categories = DATA.bibliographic_references.map((c) => c.category);
    filterContainer.innerHTML = [
      `<button type="button" class="filter-pill active" data-ref-cat="all">Todas as Categorias (13 Estudos)</button>`,
      ...categories.map((cat) => `<button type="button" class="filter-pill" data-ref-cat="${cat}">${cat}</button>`)
    ].join('');

    function renderRefs() {
      const blocks = DATA.bibliographic_references.filter(
        (b) => STATE.activeRefCategory === 'all' || b.category === STATE.activeRefCategory
      );

      gridContainer.innerHTML = blocks
        .map(
          (block) => `
        <div style="display:flex;flex-direction:column;gap:12px;margin-bottom:18px;">
          <div style="display:flex;align-items:center;gap:10px;">
            <span class="micro-badge micro-badge-vascular">PUBMED / MEDLINE</span>
            <h4 class="h4">${block.category}</h4>
          </div>
          <div class="pillars-3col-grid">
            ${block.citations
              .map(
                (cit) => `
              <article class="jn-surface-card" style="background:rgba(255,255,255,0.48);">
                <p style="font-family:var(--font-mono);font-size:0.76rem;font-weight:600;line-height:1.45;color:hsl(var(--color-dark));">
                  ${cit.citation}
                </p>
                <hr class="hr" style="margin:4px 0;">
                <p style="font-size:0.86rem;line-height:1.5;color:rgba(28,28,28,0.86);">
                  <strong>Achado & Aplicação:</strong> ${cit.key_finding}
                </p>
              </article>
            `
              )
              .join('')}
          </div>
        </div>
      `
        )
        .join('');
    }

    filterContainer.querySelectorAll('[data-ref-cat]').forEach((btn) => {
      btn.addEventListener('click', () => {
        STATE.activeRefCategory = btn.getAttribute('data-ref-cat');
        filterContainer.querySelectorAll('[data-ref-cat]').forEach((b) => b.classList.toggle('active', b === btn));
        renderRefs();
      });
    });

    renderRefs();

    // PDF Page Lightbox Preview
    document.querySelectorAll('[data-preview-pdf-page]').forEach((card) => {
      card.addEventListener('click', () => {
        const imgSrc = card.getAttribute('data-preview-pdf-page');
        const pageTitle = card.getAttribute('data-preview-title');
        const backdrop = document.getElementById('day-quickview-modal');
        const titleEl = document.getElementById('modal-day-title');
        const bodyEl = document.getElementById('modal-day-body');
        if (!backdrop || !titleEl || !bodyEl) return;

        titleEl.textContent = pageTitle;
        bodyEl.innerHTML = `
          <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;">
            <span class="caption-sm">Documento Oficial Gerado em Alta Resolução (A4)</span>
            <a href="Treino_Hipertrofia_Feminina_WilliamDelBarrio.pdf" download class="btn-pill btn-pill-dark">
              Baixar PDF Completo (7 Páginas)
            </a>
          </div>
          <div style="border:1px solid rgba(0,0,0,0.2);border-radius:8px;overflow:hidden;background:#fff;">
            <img src="${imgSrc}" alt="${pageTitle}" style="width:100%;height:auto;display:block;">
          </div>
        `;
        backdrop.classList.add('open');
        document.body.classList.add('modal-open');
      });
    });
  }

  // =========================================================================
  // 10. ANIMATED TABULAR INCREMENTORS (my-incrementor spec)
  // =========================================================================
  function initIncrementors() {
    const els = document.querySelectorAll('[data-increment-to]');
    if (!els.length) return;

    const animateEl = (el) => {
      if (el.dataset.animated === 'true') return;
      el.dataset.animated = 'true';
      const target = parseFloat(el.getAttribute('data-increment-to'));
      const decimals = parseInt(el.getAttribute('data-decimals') || '0', 10);
      const suffix = el.getAttribute('data-suffix') || '';
      const duration = 1400;
      const start = performance.now();

      const step = (now) => {
        const progress = Math.min(1, (now - start) / duration);
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = target * eased;
        el.textContent = current.toFixed(decimals).replace('.', ',') + suffix;
        if (progress < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };

    if ('IntersectionObserver' in window) {
      const obs = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              animateEl(entry.target);
              obs.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.25 }
      );
      els.forEach((el) => obs.observe(el));
    } else {
      els.forEach(animateEl);
    }
  }

  // Initialize Everything on DOMContentLoaded
  document.addEventListener('DOMContentLoaded', () => {
    initNavbarAndScrollTriggers();
    initHeroCarousel();
    renderScheduleHoloCards();
    initScheduleFilters();
    renderMasterExplorer();
    initRestTimerControls();
    initModals();
    renderScientificPillars();
    renderNitricOxideAndHydration();
    initConstancyTracker();
    initReferencesAndPdfPreview();
    initIncrementors();
  });
})();

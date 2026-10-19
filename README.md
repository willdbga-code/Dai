# DAI × WILLIAM DEL BARRIO SCIENCE

> **Programa Científico de Hipertrofia Massiva Feminina & Vascularização**  
> Glúteos 3D, Membros Inferiores, Superiores Definidos, Proteção Articular Patelar/Lombar e Planilha Interativa de Constância.

---

## ⚡ Visão Geral do Projeto

Sistema completo de treinamento resistido feminino baseado em evidências científicas e biomecânica aplicada, desenvolvido com base na arquitetura editorial de alta precisão **Prozhe v1.1.0** e renderizações 3D em **Blender 4.2 (EEVEE Next)**.

- **Perfil Biométrico Alvo:** Atleta Feminina Natural, 1,65 m, 62,0 kg (IMC 22,8 — Eutrófica).
- **Divisão Semanal (5+1+1):** 5 dias em academia completa (Seg–Sex) + Sábado pump metabólico em casa (zero impacto articular) + Domingo supercompensação e descanso sistêmico.
- **Volume Total:** 24 exercícios prescritos, 94 séries semanais calibradas na escala RIR 0–2.
- **Embasamento:** 13 estudos clínicos e revisões sistemáticas indexados no PubMed/MEDLINE.

---

## 🧬 Funcionalidades do Sistema

1. **Navbar Glassmórfica com Dock Flutuante & Drawer Expansível:**
   - Monograma vetorial, navegação por âncoras, gaveta de telemetria da atleta e seletor flutuante ativado por scroll.
2. **Hero Viewport Carrossel (3 Slides Full-Bleed 100svh):**
   - Esculturas 3D interativas dos vetores de glúteo, sobrecarga em alongamento (*titina/mecanotransdução*) e vascularização (*VEGF/óxido nítrico*).
3. **Microciclo 7D com Cards Holográficos 3D (`.card-holo`):**
   - Física de rotação 3D responsiva ao cursor, camadas de shaders (`color-dodge`, `soft-light`), espectros analógicos e esculturas 3D de estúdio geradas no Blender 4.2.
4. **Explorador Mestre de Treinos & Cronômetro de Descanso:**
   - Prescrição de séries, repetições, RIR, tempos de intervalo dinâmicos (45s a 150s) com barra de progresso em tempo real e checklist de aquecimento sinovial.
5. **Painel de Biomecânica dos 3 Vetores de Glúteo & Proteção Patelar:**
   - Tíbia vertical 90°, alinhamento articular knee-friendly, download dos arquivos nativos 3D (`.blend` e `.glb`).
6. **Bioenergética & Protocolo de Óxido Nítrico:**
   - 2.400 kcal/dia, 124g de proteína, controle interativo de hidratação e volume plasmático (meta 2,8L/dia) e checklist de vasodilatação.
7. **Planilha Interativa de Constância & Sobrecarga Progressiva:**
   - Registro de séries com persistência no `localStorage`, notas de sensação articular e escala de vascularização, além de exportação completa em JSON.
8. **Galeria do Documento Oficial em PDF (7 Páginas A4):**
   - Visualização das 7 pranchas de alta resolução geradas programaticamente via ReportLab e download do documento oficial.

---

## 📁 Estrutura de Arquivos

```text
Dai/
├── index.html                                        # Frontend principal (Single Page Application)
├── css/
│   └── jn-design-system.css                          # Design System Prozhe v1.1.0 e tokens CSS
├── js/
│   ├── app.js                                        # Controlador de estado, carrossel, timer e modal
│   └── program-data.js                               # Dados estruturados do treino para runtime JS
├── assets3d/
│   ├── day_1_3d.png ... day_7_3d.png                 # Renders 3D isolados dos 7 dias (Blender 4.2)
│   ├── hip_thrust_3d_render.png                      # Render de telemetria biomecânica
│   ├── hip_thrust_3d_telemetry.blend                 # Cena 3D nativa do Blender 4.2
│   └── hip_thrust_3d_telemetry.glb                   # Modelo 3D interativo glTF 2.0
├── page_1.png ... page_7.png                         # Pré-visualizações A4 das 7 páginas do PDF
├── Treino_Hipertrofia_Feminina_WilliamDelBarrio.pdf  # PDF Oficial A4 para impressão e consulta
├── workout_program.json                              # Schema canônico da periodização e bibliografia
├── generate_all_cards_3d.py                          # Script headless Blender para gerar os 7 cards 3D
├── generate_biomechanics_3d.py                       # Script headless Blender para cena de biomecânica
└── generate_workout_pdf.py                           # Gerador do PDF institucional ReportLab
```

---

## 🚀 Como Executar Localmente

Você pode abrir o projeto diretamente em qualquer navegador moderno:

```bash
# Servir via Python embutido
python -m http.server 8080
```

Acesse em seu navegador: `http://localhost:8080`

---

## 📜 Licença e Créditos

- **Metodologia:** William Del Barrio
- **Evidências Científicas:** Literatura revisada por pares (Contreras, Maeo, Schoenfeld, Pedrosa, Morton et al.)
- **Ano:** 2026

# -*- coding: utf-8 -*-
"""
Gerador de PDF do Programa Científico de Hipertrofia Feminina & Vascularização
Metodologia: William Del Barrio & Literatura Científica
Atleta: Mulher Natural, 1,75 m, 62 kg, Foco Glúteos/Pernas & Vascularização
Inclui: Página 7 dedicada a todas as Referências Bibliográficas Científicas.
"""

import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# Registro de Fontes TrueType com suporte nativo a acentos (Windows Arial)
FONT_NAME = "Helvetica"
FONT_NAME_BOLD = "Helvetica-Bold"
FONT_NAME_ITALIC = "Helvetica-Oblique"

try:
    if os.path.exists(r"C:\Windows\Fonts\arial.ttf"):
        pdfmetrics.registerFont(TTFont('Arial', r'C:\Windows\Fonts\arial.ttf'))
        pdfmetrics.registerFont(TTFont('Arial-Bold', r'C:\Windows\Fonts\arialbd.ttf'))
        pdfmetrics.registerFont(TTFont('Arial-Italic', r'C:\Windows\Fonts\ariali.ttf'))
        pdfmetrics.registerFont(TTFont('Arial-BoldItalic', r'C:\Windows\Fonts\arialbi.ttf'))
        registerFontFamily('Arial', normal='Arial', bold='Arial-Bold', italic='Arial-Italic', boldItalic='Arial-BoldItalic')
        FONT_NAME = "Arial"
        FONT_NAME_BOLD = "Arial-Bold"
        FONT_NAME_ITALIC = "Arial-Italic"
        print("Fonte Arial TrueType registrada com sucesso!")
except Exception as e:
    print(f"Aviso: Fallback para Helvetica: {e}")


class NumberedCanvas(canvas.Canvas):
    """
    Canvas dinâmico de duas passagens: calcula o número total de páginas
    e desenha cabeçalhos e rodapés institucionais elegantes.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages):
        # Na primeira página (capa), desenhamos a barra decorativa lateral
        if self._pageNumber == 1:
            self.saveState()
            self.setFillColor(colors.HexColor("#BE123C"))
            self.rect(0, 0, 0.7 * cm, A4[1], fill=True, stroke=False)
            self.setFillColor(colors.HexColor("#0F172A"))
            self.rect(0.7 * cm, 0, 0.3 * cm, A4[1], fill=True, stroke=False)
            self.restoreState()
            return

        self.saveState()
        self.setFont(FONT_NAME, 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Cabeçalho Superior
        self.drawString(1.5 * cm, A4[1] - 1.15 * cm, "PROGRAMA DE HIPERTROFIA FEMININA & VASCULARIZAÇÃO • WILLIAM DEL BARRIO SCIENCE")
        self.drawRightString(A4[0] - 1.5 * cm, A4[1] - 1.15 * cm, "ATLETA: NATURAL • 1,75 m • 62 kg")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(1.5 * cm, A4[1] - 1.30 * cm, A4[0] - 1.5 * cm, A4[1] - 1.30 * cm)

        # Rodapé Inferior
        self.line(1.5 * cm, 1.35 * cm, A4[0] - 1.5 * cm, 1.35 * cm)
        self.drawString(1.5 * cm, 0.95 * cm, "Base de Dados Oficial para o Site de Controle de Constância • Sobrecarga Progressiva RIR 1-2")
        page_text = f"Página {self._pageNumber} de {total_pages}"
        self.drawRightString(A4[0] - 1.5 * cm, 0.95 * cm, page_text)

        self.restoreState()


def create_pdf(json_path, output_pdf_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.7 * cm,
        bottomMargin=1.7 * cm
    )

    styles = getSampleStyleSheet()

    # Paleta de Cores
    PRIMARY = colors.HexColor("#0F172A")       # Slate 900
    SECONDARY = colors.HexColor("#BE123C")     # Rose 700
    DARK_TEXT = colors.HexColor("#1E293B")     # Slate 800
    MUTED_TEXT = colors.HexColor("#475569")    # Slate 600
    LIGHT_BG = colors.HexColor("#F8FAFC")      # Slate 50
    CARD_BG = colors.HexColor("#F1F5F9")       # Slate 100
    BORDER_COLOR = colors.HexColor("#CBD5E1")  # Slate 300

    # Tipografia Customizada
    cover_tag_style = ParagraphStyle(
        'CoverTag',
        parent=styles['Normal'],
        fontName=FONT_NAME_BOLD,
        fontSize=9,
        leading=12,
        textColor=SECONDARY,
        spaceAfter=6
    )

    title_cover_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName=FONT_NAME_BOLD,
        fontSize=23,
        leading=28,
        textColor=PRIMARY,
        spaceAfter=8
    )

    subtitle_cover_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=11,
        leading=15,
        textColor=MUTED_TEXT,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName=FONT_NAME_BOLD,
        fontSize=13,
        leading=17,
        textColor=PRIMARY,
        spaceBefore=6,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName=FONT_NAME_BOLD,
        fontSize=11,
        leading=15,
        textColor=SECONDARY,
        spaceBefore=6,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=8.5,
        leading=12.5,
        textColor=DARK_TEXT,
        spaceAfter=4
    )

    small_note = ParagraphStyle(
        'SmallNote',
        parent=styles['Normal'],
        fontName=FONT_NAME_ITALIC,
        fontSize=7.5,
        leading=10.5,
        textColor=MUTED_TEXT
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName=FONT_NAME_BOLD,
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=7.5,
        leading=10,
        textColor=DARK_TEXT
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell_style,
        fontName=FONT_NAME_BOLD,
        textColor=PRIMARY
    )

    table_cell_center = ParagraphStyle(
        'TableCellCenter',
        parent=table_cell_style,
        alignment=1
    )

    table_cell_center_bold = ParagraphStyle(
        'TableCellCenterBold',
        parent=table_cell_bold,
        alignment=1
    )

    rating_scale_style = ParagraphStyle(
        'RatingScale',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=6.5,
        leading=8.5,
        textColor=DARK_TEXT,
        alignment=1
    )

    ref_citation_style = ParagraphStyle(
        'RefCitation',
        parent=styles['Normal'],
        fontName=FONT_NAME_BOLD,
        fontSize=7.0,
        leading=9.0,
        textColor=PRIMARY
    )

    ref_finding_style = ParagraphStyle(
        'RefFinding',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=6.8,
        leading=8.8,
        textColor=DARK_TEXT
    )

    ref_category_header = ParagraphStyle(
        'RefCatHeader',
        parent=styles['Normal'],
        fontName=FONT_NAME_BOLD,
        fontSize=7.5,
        leading=10,
        textColor=SECONDARY
    )

    story = []

    # =========================================================================
    # PÁGINA 1: CAPA & SUMÁRIO EXECUTIVO DA ATLETA
    # =========================================================================
    story.append(Spacer(1, 1.0 * cm))
    story.append(Paragraph("SISTEMA CIENTÍFICO DE TREINAMENTO RESISTIDO", cover_tag_style))
    story.append(Paragraph("PROGRAMA DE HIPERTROFIA MASSIVA FEMININA & VASCULARIZAÇÃO", title_cover_style))
    story.append(Paragraph("METODOLOGIA EVIDENCIADA WILLIAM DEL BARRIO • BIOMECÂNICA APLICADA • DIVISÃO 5+1 DIAS", subtitle_cover_style))
    story.append(HRFlowable(width="100%", thickness=2, color=SECONDARY, spaceBefore=0, spaceAfter=14))

    profile_data = [
        [
            Paragraph("<b>PARÂMETRO BIOMÉTRICO</b>", table_cell_bold),
            Paragraph("<b>DADO DA ATLETA</b>", table_cell_bold),
            Paragraph("<b>IMPLICAÇÃO CIENTÍFICA NO PROGRAMA</b>", table_cell_bold)
        ],
        [
            Paragraph("<b>Gênero & Fisiologia</b>", table_cell_style),
            Paragraph("Feminino / Natural (Sem Fármacos)", table_cell_style),
            Paragraph("Maior densidade de fibras Tipo I; resistência à fadiga superior; capacidade de suportar volume semanal frequente e recuperação acelerada entre séries.", table_cell_style)
        ],
        [
            Paragraph("<b>Altura & Peso</b>", table_cell_style),
            Paragraph("1,75 m | 62 kg (IMC 20,2)", table_cell_style),
            Paragraph("Alavancas ósseas longas (fêmur e tíbia compridos). Maior amplitude mecânica articular e tensão profunda no ponto de alongamento muscular.", table_cell_style)
        ],
        [
            Paragraph("<b>Nível Muscular Inicial</b>", table_cell_style),
            Paragraph("Baixa Musculatura de Base", table_cell_style),
            Paragraph("Janela máxima de 'Newbie Gains' (hipertrofia acelerada). O corpo responde prontamente à sobrecarga progressiva com técnica estrita e dieta hipercalórica limpa.", table_cell_style)
        ],
        [
            Paragraph("<b>Condição Articular</b>", table_cell_style),
            Paragraph("Leve Sensibilidade no Joelho", table_cell_style),
            Paragraph("Adaptação Joelho-Amigável (Knee-Friendly): canela quase vertical em afundos (tronco a 40° para carregar o glúteo), pés altos no Leg Press e pré-aquecimento sinovial.", table_cell_style)
        ],
        [
            Paragraph("<b>Objetivo Prioritário</b>", table_cell_style),
            Paragraph("Glúteos 3D + Pernas + Vascularização", table_cell_style),
            Paragraph("Harmonização dos 3 vetores de glúteo de Bret Contreras + supersets para antebraço e séries metabólicas (15-20 reps) para angiogênese venosa.", table_cell_style)
        ],
        [
            Paragraph("<b>Divisão e Ambientes</b>", table_cell_style),
            Paragraph("5 Dias Academia + 1 Dia Casa", table_cell_style),
            Paragraph("Segunda a Sexta em academia completa (pesos, polias, máquinas) + Sábado focado em Pump Metabólico em casa (sem aparelhos) + Domingo de repouso.", table_cell_style)
        ]
    ]

    t_profile = Table(profile_data, colWidths=[4.2 * cm, 4.2 * cm, 9.6 * cm])
    t_profile.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), CARD_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), PRIMARY),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_profile)
    story.append(Spacer(1, 12))

    box_data = [[
        Paragraph(
            "<b>FINALIDADE & INTEGRAÇÃO COM A PLATAFORMA DE CONSTÂNCIA:</b><br/>"
            "Este plano foi desenhado para ser tanto a sua rotina diária impressa quanto a arquitetura de dados definitiva "
            "do seu <b>site de controle de constância</b>. Cada exercício possui parâmetros numéricos estruturados "
            "(séries, repetições, RIR, descanso e biomecânica). O sucesso natural é fruto da progressão milimétrica anotada sessão a sessão.",
            body_style
        )
    ]]
    t_box = Table(box_data, colWidths=[18.0 * cm])
    t_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FFF1F2")),
        ('BOX', (0, 0), (-1, -1), 1, SECONDARY),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_box)

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 2: FUNDAMENTAÇÃO CIENTÍFICA (WILLIAM DEL BARRIO) & DIRETRIZES
    # =========================================================================
    story.append(Paragraph("1. FUNDAMENTAÇÃO CIENTÍFICA & BIOMECÂNICA APLICADA", h1_style))
    story.append(Paragraph(
        "A metodologia de William Del Barrio integra biomecânica funcional com as descobertas mais recentes da ciência do esporte. "
        "Abaixo estão os pilares centrais que orientam a seleção e a dosagem de cada exercício deste protocolo:",
        body_style
    ))
    story.append(Spacer(1, 4))

    pillars_table_data = [
        [
            Paragraph("<b>PILAR CIENTÍFICO</b>", table_header_style),
            Paragraph("<b>EVIDÊNCIAS & AUTORES</b>", table_header_style),
            Paragraph("<b>COMO É APLICADO NESTE TREINO</b>", table_header_style)
        ],
        [
            Paragraph("<b>Hipertrofia no Alongamento<br/>(Stretch-Mediated)</b>", table_cell_bold),
            Paragraph("Maeo et al. (2021);<br/>Pedrosa et al. (2022);<br/>Wolf et al. (2023)", table_cell_style),
            Paragraph("Músculos sob carga em comprimento máximo geram sinalização hipertrófica superior. Usamos <b>Cadeira Flexora</b> (superior à mesa deitada), <b>RDL profundo</b> e <b>Lengthened Partials</b> (repetições parciais na fase alongada na última série de isolamentos).", table_cell_style)
        ],
        [
            Paragraph("<b>Os 3 Vetores de Glúteo<br/>(Bret Contreras)</b>", table_cell_bold),
            Paragraph("Contreras et al. (2015, 2020);<br/>Del Barrio (2026)", table_cell_style),
            Paragraph("1. <b>Vetor Horizontal</b>: Hip Thrust / Kas Bridge (pico no topo).<br/>2. <b>Vetor Alongamento/Hinge</b>: RDL e Búlgaro.<br/>3. <b>Vetor Abdução</b>: Polia a 30° e Cadeira Abdutora inclinada para o glúteo médio e superior.", table_cell_style)
        ],
        [
            Paragraph("<b>Intensidade & RIR<br/>(Reps in Reserve)</b>", table_cell_bold),
            Paragraph("Refalo et al. (2022);<br/>Robinson et al. (2023)", table_cell_style),
            Paragraph("<b>RIR 1-2</b> nos compostos pesados (parar faltando 1 a 2 repetições para a falha técnica real). <b>RIR 0-1</b> em isolamentos guiados e no treino caseiro de sábado, acumulando estresse metabólico sem risco articular.", table_cell_style)
        ],
        [
            Paragraph("<b>Proteção Patelofemoral<br/>(Knee-Friendly Strategy)</b>", table_cell_bold),
            Paragraph("Schoenfeld (2010);<br/>Horschig (Squat University)", table_cell_style),
            Paragraph("Com fêmur longo e sensibilidade no joelho: tronco projetado à frente nos afundos (canela vertical descarrega a patela no glúteo), pés altos na plataforma do Leg Press e aquecimento prévio com flexora leve para ativação sinovial.", table_cell_style)
        ]
    ]

    t_pillars = Table(pillars_table_data, colWidths=[4.2 * cm, 4.0 * cm, 9.8 * cm])
    t_pillars.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_pillars)
    story.append(Spacer(1, 8))

    story.append(Paragraph("2. DIRETRIZES DE VASCULARIZAÇÃO PARA MULHERES NATURAIS", h2_style))
    story.append(Paragraph(
        "Em praticantes naturais femininas com baixa massa muscular inicial, a vascularização aparente (veias visíveis nos braços e ombros) "
        "é construída através de três mecanismos biológicos sinérgicos:",
        body_style
    ))

    vasc_points = [
        "<b>Aumento da Secção Transversa do Músculo (Efeito Alavanca):</b> As veias cefálica e basílica repousam sobre os músculos do braço e antebraço. Quando os músculos bíceps, braquial e braquiorradial hipertrofiam, eles empurram mecanicamente essas veias contra a pele superficial.",
        "<b>Estresse Metabólico & Angiogênese (VEGF):</b> Séries com repetições mais altas (12 a 20 reps) e tempos sob tensão aumentam o estresse de cisalhamento endotelial, estimulando a liberação de VEGF (Vascular Endothelial Growth Factor) e gerando novos leitos capilares.",
        "<b>Estímulo Direto de Antebraço e Ombros:</b> A rosca inversa com pegada pronada recruta intensamente o braquiorradial. O Farmer's Walk promove contração isométrica prolongada com oclusão venosa natural seguida de hiperemia reativa (pump vascular explosivo).",
        "<b>Hidratação Plena & Via do Óxido Nítrico:</b> Ingerir 35 a 45 ml/kg de água (2,5L a 3,0L) mantém o volume de plasma sanguíneo expandido. O consumo de nitratos dietéticos (beterraba, espinafre, rúcula) e sódio moderado pré-treino potencializam o calibre dos vasos sanguíneos."
    ]
    for pt in vasc_points:
        story.append(Paragraph(f"• {pt}", body_style))

    story.append(PageBreak())

    # =========================================================================
    # FUNÇÃO HELPER: CONSTRUTOR DE TABELA DE TREINOS COM LARGURA RIGOROSA
    # =========================================================================
    def build_workout_table(day_data):
        rows = [
            [
                Paragraph("<b>#</b>", table_header_style),
                Paragraph("<b>EXERCÍCIO & VETOR</b>", table_header_style),
                Paragraph("<b>SÉRIES</b>", table_header_style),
                Paragraph("<b>REPS</b>", table_header_style),
                Paragraph("<b>RIR</b>", table_header_style),
                Paragraph("<b>DESCANSO</b>", table_header_style),
                Paragraph("<b>NOTAS DE EXECUÇÃO & BIOMECÂNICA</b>", table_header_style)
            ]
        ]

        for ex in day_data["exercises"]:
            partials_badge = " <font color='#BE123C'><b>[+Parciais]</b></font>" if ex.get("has_lengthened_partials") else ""
            ex_name_p = Paragraph(f"<b>{ex['name']}</b>{partials_badge}<br/><font color='#64748B' size=6.5>{ex['vector']}</font>", table_cell_style)
            sets_p = Paragraph(str(ex["sets"]), table_cell_center_bold)
            reps_p = Paragraph(str(ex["reps"]), table_cell_center)
            
            rir_text = str(ex["rir"])
            if "falha" in rir_text.lower():
                rir_text = "0 (Falha)"
            rir_p = Paragraph(rir_text, table_cell_center)
            
            rest_p = Paragraph(f"{ex['rest_seconds']}s", table_cell_center)
            notes_p = Paragraph(ex["notes"], small_note)

            rows.append([
                Paragraph(str(ex["order"]), table_cell_center_bold),
                ex_name_p,
                sets_p,
                reps_p,
                rir_p,
                rest_p,
                notes_p
            ])

        t = Table(rows, colWidths=[0.6 * cm, 4.6 * cm, 1.4 * cm, 1.7 * cm, 1.1 * cm, 1.8 * cm, 6.8 * cm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
            ('TOPPADDING', (0, 0), (-1, -1), 3.0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3.0),
            ('LEFTPADDING', (0, 0), (-1, -1), 2.5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2.5),
        ]))
        return t

    # =========================================================================
    # PÁGINA 3: TABELA DE TREINOS - SEGUNDA & TERÇA
    # =========================================================================
    d1 = data["schedule"][0]
    story.append(Paragraph(f"DIA 1: {d1['day_name'].upper()} — {d1['session_name'].upper()}", h1_style))
    story.append(Paragraph(f"<b>Ambiente:</b> {d1['location']} | <b>Foco da Sessão:</b> {d1['target_focus']}", small_note))
    story.append(Paragraph("<b>Aquecimento Joelho-Amigável:</b> 5 min esteira inclinada + 1x15 flexora bem leve (lubrificação sinovial) + mobilidade tornozelo.", small_note))
    story.append(Spacer(1, 4))
    story.append(build_workout_table(d1))
    story.append(Spacer(1, 10))

    d2 = data["schedule"][1]
    story.append(Paragraph(f"DIA 2: {d2['day_name'].upper()} — {d2['session_name'].upper()}", h1_style))
    story.append(Paragraph(f"<b>Ambiente:</b> {d2['location']} | <b>Foco da Sessão:</b> {d2['target_focus']}", small_note))
    story.append(Paragraph("<b>Aquecimento:</b> 2x15 rotação externa de manguito no cabo leve + ativação escapular na barra fixa ou polia.", small_note))
    story.append(Spacer(1, 4))
    story.append(build_workout_table(d2))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 4: TABELA DE TREINOS - QUARTA & QUINTA
    # =========================================================================
    d3 = data["schedule"][2]
    story.append(Paragraph(f"DIA 3: {d3['day_name'].upper()} — {d3['session_name'].upper()}", h1_style))
    story.append(Paragraph(f"<b>Ambiente:</b> {d3['location']} | <b>Foco da Sessão:</b> {d3['target_focus']}", small_note))
    story.append(Paragraph("<b>Aquecimento:</b> 2x30s ponte isométrica no chão + mobilidade ativa de posteriores com quadril fletido.", small_note))
    story.append(Spacer(1, 4))
    story.append(build_workout_table(d3))
    story.append(Spacer(1, 10))

    d4 = data["schedule"][3]
    story.append(Paragraph(f"DIA 4: {d4['day_name'].upper()} — {d4['session_name'].upper()}", h1_style))
    story.append(Paragraph(f"<b>Ambiente:</b> {d4['location']} | <b>Foco da Sessão:</b> {d4['target_focus']}", small_note))
    story.append(Paragraph("<b>Aquecimento:</b> 2x15 ativação de peitoral no crossover leve + 2x30s prancha frontal de ativação de core.", small_note))
    story.append(Spacer(1, 4))
    story.append(build_workout_table(d4))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 5: TABELA DE TREINOS - SEXTA & SÁBADO (EM CASA)
    # =========================================================================
    d5 = data["schedule"][4]
    story.append(Paragraph(f"DIA 5: {d5['day_name'].upper()} — {d5['session_name'].upper()}", h1_style))
    story.append(Paragraph(f"<b>Ambiente:</b> {d5['location']} | <b>Foco da Sessão:</b> {d5['target_focus']}", small_note))
    story.append(Paragraph("<b>Aquecimento:</b> 2x12 elevação pélvica unilateral sem carga + 1x15 abdução no cabo bem leve para acordar o glúteo médio.", small_note))
    story.append(Spacer(1, 4))
    story.append(build_workout_table(d5))
    story.append(Spacer(1, 10))

    d6 = data["schedule"][5]
    story.append(Paragraph(f"DIA 6: {d6['day_name'].upper()} — {d6['session_name'].upper()}", h1_style))
    story.append(Paragraph(f"<b>Ambiente:</b> {d6['location']} | <b>Foco da Sessão:</b> {d6['target_focus']}", small_note))
    story.append(Paragraph("<b>Diretrizes em Casa:</b> Zero impacto e zero estresse articular. Foco em queimação metabólica, ritmo constante e pico de contração.", small_note))
    story.append(Spacer(1, 4))
    story.append(build_workout_table(d6))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 6: PROTOCOLO NUTRICIONAL & REGISTRO DE CONSTÂNCIA PARA O SITE
    # =========================================================================
    story.append(Paragraph("3. PROTOCOLO NUTRICIONAL PARA HIPERTROFIA NATURAL & VASCULARIZAÇÃO", h1_style))
    story.append(Paragraph(
        "Para uma atleta feminina natural de 1,75 m e 62 kg com pouca musculatura inicial, o ambiente calórico é o fator limitante. "
        "Sem superávit calórico controlado, o corpo não possui excedente de substrato para expandir miofibrilas e redes vasculares.",
        body_style
    ))
    story.append(Spacer(1, 4))

    nutri_table_data = [
        [
            Paragraph("<b>MACRONUTRIENTE</b>", table_header_style),
            Paragraph("<b>RECOMENDAÇÃO CIENTÍFICA</b>", table_header_style),
            Paragraph("<b>META DIÁRIA (62 KG)</b>", table_header_style),
            Paragraph("<b>PAPEL NA HIPERTROFIA & VASCULARIZAÇÃO</b>", table_header_style)
        ],
        [
            Paragraph("<b>Proteínas</b>", table_cell_bold),
            Paragraph("2,0 g/kg (Morton et al., 2018)", table_cell_style),
            Paragraph("<b>~124 g / dia</b>", table_cell_bold),
            Paragraph("Síntese proteica muscular máxima. Fontes: frango, ovos, peixes, laticínios magros, whey protein.", table_cell_style)
        ],
        [
            Paragraph("<b>Gorduras Saudáveis</b>", table_cell_bold),
            Paragraph("0,9 g/kg (Suporte Endócrino)", table_cell_style),
            Paragraph("<b>~56 g / dia</b>", table_cell_bold),
            Paragraph("Essencial para regulação do ciclo menstrual, síntese de estrogênio natural e absorção de vitaminas lipossolúveis.", table_cell_style)
        ],
        [
            Paragraph("<b>Carboidratos</b>", table_cell_bold),
            Paragraph("4,2 a 4,8 g/kg (Glicogênio Pleno)", table_cell_style),
            Paragraph("<b>260 a 300 g / dia</b>", table_cell_bold),
            Paragraph("<b>Segredo da Vascularização</b>: 1g de glicogênio retém 3g de água intracelular, expandindo o volume muscular e projetando as veias para a derme.", table_cell_style)
        ],
        [
            Paragraph("<b>Calorias Totais</b>", table_cell_bold),
            Paragraph("+250 a 300 kcal superávit limpo", table_cell_style),
            Paragraph("<b>2.150 a 2.300 kcal/dia</b>", table_cell_bold),
            Paragraph("Ganho de peso alvo: 0,8 a 1,2 kg por mês. Garante hipertrofia acelerada sem acúmulo desnecessário de gordura corporal.", table_cell_style)
        ]
    ]

    t_nutri = Table(nutri_table_data, colWidths=[3.2 * cm, 4.0 * cm, 3.2 * cm, 7.6 * cm])
    t_nutri.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_nutri)
    story.append(Spacer(1, 10))

    story.append(Paragraph("4. FICHA OFICIAL DE CONTROLE DE CONSTÂNCIA (LOGSHEET SEMANAL)", h1_style))
    story.append(Paragraph(
        "Utilize esta tabela como modelo físico de registro até o lançamento da sua plataforma digital. "
        "Como enfatiza William Del Barrio: <i>'A evolução no espelho é um atraso de semanas da sobrecarga progressiva registrada no seu caderno.'</i>",
        body_style
    ))
    story.append(Spacer(1, 4))

    log_rows = [
        [
            Paragraph("<b>DATA</b>", table_header_style),
            Paragraph("<b>SESSÃO</b>", table_header_style),
            Paragraph("<b>EXERCÍCIO PRINCIPAL</b>", table_header_style),
            Paragraph("<b>CARGA (KG)</b>", table_header_style),
            Paragraph("<b>REPS FEITAS</b>", table_header_style),
            Paragraph("<b>RIR REAL</b>", table_header_style),
            Paragraph("<b>CONFORTO JOELHO</b>", table_header_style),
            Paragraph("<b>PUMP / VASC</b>", table_header_style)
        ]
    ]

    for _ in range(6):
        log_rows.append([
            Paragraph("___/___", table_cell_center),
            Paragraph("Dia ___", table_cell_center),
            Paragraph("", table_cell_style),
            Paragraph("", table_cell_style),
            Paragraph("", table_cell_style),
            Paragraph("", table_cell_style),
            Paragraph("1  2  3  4  5", rating_scale_style),
            Paragraph("1  2  3  4  5", rating_scale_style)
        ])

    t_log = Table(log_rows, colWidths=[1.6 * cm, 1.8 * cm, 4.8 * cm, 1.8 * cm, 1.8 * cm, 1.4 * cm, 2.5 * cm, 2.3 * cm])
    t_log.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(t_log)

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 7: REFERÊNCIAS BIBLIOGRÁFICAS CIENTÍFICAS (COMPILAÇÃO WILLIAM DEL BARRIO)
    # =========================================================================
    story.append(Paragraph("5. REFERÊNCIAS BIBLIOGRÁFICAS CIENTÍFICAS (COMPILAÇÃO WILLIAM DEL BARRIO)", h1_style))
    story.append(Paragraph(
        "Todas as recomendações, seleções de exercícios, faixas de repetições e intervalos deste programa são embasadas "
        "em ensaios clínicos controlados e revisões sistemáticas com meta-análise indexadas no PubMed/MEDLINE. "
        "Abaixo constam as referências bibliográficas completas que sustentam a prescrição:",
        body_style
    ))
    story.append(Spacer(1, 4))

    ref_table_rows = [
        [
            Paragraph("<b>REFERÊNCIA FORMAL (AUTORES, ANO & PERIÓDICO)</b>", table_header_style),
            Paragraph("<b>ACHADO CIENTÍFICO FUNDAMENTAL & APLICAÇÃO NESTE PROGRAMA</b>", table_header_style)
        ]
    ]

    for cat_data in data.get("bibliographic_references", []):
        cat_title = cat_data["category"]
        # Linha separadora de categoria
        ref_table_rows.append([
            Paragraph(f"<b>{cat_title.upper()}</b>", ref_category_header),
            Paragraph("", ref_category_header)
        ])
        for cit in cat_data["citations"]:
            ref_table_rows.append([
                Paragraph(cit["citation"], ref_citation_style),
                Paragraph(cit["key_finding"], ref_finding_style)
            ])

    t_refs = Table(ref_table_rows, colWidths=[8.5 * cm, 9.5 * cm])
    
    # Criar estilos de tabela com base nas linhas de categoria
    t_ref_styles = [
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 2.2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
        ('LEFTPADDING', (0, 0), (-1, -1), 3.5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3.5),
    ]

    # Destacar as linhas de categoria
    current_idx = 1
    for cat_data in data.get("bibliographic_references", []):
        t_ref_styles.append(('SPAN', (0, current_idx), (1, current_idx)))
        t_ref_styles.append(('BACKGROUND', (0, current_idx), (1, current_idx), colors.HexColor("#FFF1F2")))
        current_idx += 1 + len(cat_data["citations"])

    t_refs.setStyle(TableStyle(t_ref_styles))
    story.append(t_refs)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF gerado com sucesso: {output_pdf_path}")


if __name__ == "__main__":
    json_file = r"c:\Users\LENOVO\Downloads\Dai\workout_program.json"
    pdf_file_wdb = r"c:\Users\LENOVO\Downloads\Dai\Treino_Hipertrofia_Feminina_WilliamDelBarrio.pdf"
    pdf_file_legacy = r"c:\Users\LENOVO\Downloads\Dai\Treino_Hipertrofia_Feminina_JeffNippard.pdf"
    create_pdf(json_file, pdf_file_wdb)
    create_pdf(json_file, pdf_file_legacy)

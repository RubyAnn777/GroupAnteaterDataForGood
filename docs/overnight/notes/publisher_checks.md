# Publisher-side checks (2026-10-10, Chrome, anonymous)

## A. MAAP pages (saved as rendered text, NOT raw HTML)
Raw HTML could not be saved: a local receiver for POSTing outerHTML was blocked by the permission classifier, and returning full HTML through the tool output was impractical. Files are therefore text only, and #130, #193, #208 are abridged (omitted parts marked in each file); #241 is verified excerpts only. They are evidence of what was read, not a faithful archive. A human should still use browser "Save as" for raw HTML.

| MAAP | File | sha256 | Status |
|---|---|---|---|
| #130 | data_raw/maap/maap_130.txt | 552b05b280ee1dfcbe3ac4ef6d24fa22740230580996d40262fa22e5d36ad549 | OK: 4,450->300 ha; 165->17 ha/mo, 90%; 1,115 vs 6,490 ha; Camanti 336->105 all confirmed. Headline 78% vs citation line 79% confirmed |
| #193 | data_raw/maap/maap_193.txt | 94aa241cdf19ea0db3f59d74a9b58e1e35ca785726ad27926582e76b71cd65de | OK: 148->598 dredges; 592->2,392 people; 788 ha ponds, +2,550 ha. No English version exists (English slug and "English" switcher do not give one) |
| #208 | data_raw/maap/maap_208.txt | 2c1242fc392e9dfbb98564890e75498f9808c6f3521d052919918cad3698820f | OK: 30,846 ha; 74% / 73.8% (22,756); buffer zones 2,439 ha (7.9%); 4,494 ha native communities |
| #241 | data_raw/maap/maap_241.txt | e872f4d094334505ca130649393d343d2ef7c7224358fc0af482f7b56dbee84c | OK: 500 ha (431 + 69); emergency since 7 Apr 2023 DS 046-2023-PCM; navy withdrawn 2025; 2017-18 operations sentence |

Discrepancies noted (none contradict maap_citations.md):
- #193: "aumento de más del 400%" for 148 -> 598 dragas is arithmetically +304% (4.04x). Cite counts, not the percentage, or say "about four times".
- #193: 788 ha / "+2,550 ha (>320%)": 2,550/788 = 324%, so 2,550 is the increment (new total about 3,338 ha), resolving the ambiguity flagged in maap_citations.md. Inference from arithmetic, not stated by MAAP.
- #208: Barranco Chico 1,008 ha (list) vs 967 ha (text, "last three years"). Minor internal inconsistency in MAAP.

## B. MapBiomas platform checks
| Item | Status | Seen | Expected | Evidence |
|---|---|---|---|---|
| Peru, Reserva Nacional Tambopata (Natural Protected Area), Mining 2025, Col. 4 | OK | 777 ha (tooltip rounds) | 776.9 | data_raw/mapbiomas_peru/platform_check_tambopata_2026-10-10.txt + platform_check_tambopata_reserve_2026-10-10.jpg |
| Peru, Tambopata buffer zone, Mining 2025, Col. 4 | OK | 20,730 ha | 20,730 | same .txt + platform_check_tambopata_bufferzone_2026-10-10.jpg |
| Brazil, Kayapó TI, Mining 2024 | MISMATCH (collection) | 17,632 ha (2025: 18,573) in Collection 11 | ~18,176 (Col 10.1) | data_raw/mapbiomas_brazil/platform_check_kayapo_2026-10-10.txt + .jpg |
| Brazil, Yanomami | NOT DONE | | 4,576 (2024), 3,573 (2022) | |

Brazil platform offers only Collection 11 (note updated 08/2026) and FUNAI 2026 boundaries; Collection 10.1 is not selectable. So the -3% gap is expected and not a check failure; the Col 10.1 numbers must be checked against the Col 10.1 statistics download. Never mix Col 11 platform values into the Col 10.1 series.

Click paths: see the .txt files. Peru: Group by > Natural Protected Area (or Buffer zone) > search Tambopata > Apply > legend "Mining" > time series, hover 2025. Brazil: Group by > Terras Indígenas > search Kayapó > Apply > legend "Mining" > time series, hover.

Firecrawl calls this run: 0. Chrome tab opened by me was closed.

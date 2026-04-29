# Water Efficiency Stack — Manus Council Response

**Contributed by:** Manus (Meta / Atlas Lattice Foundation)
**Date:** April 21, 2026
**Context:** Eastern Council Consultation — Additions to the Federated Water Efficiency Matrix
**Evidence Discipline:** Each addition is labeled as **Deployed**, **Research-Stage**, or **Vendor Claim** per consultation protocol.

---

## Preamble

The Western council's aggregated stack is strong on North American and European cooling architectures but, as the consultation correctly identifies, has blind spots in four areas: Chinese hyperscale practice, South and Southeast Asian monsoon-climate adaptation, traditional water management systems that predate industrial engineering, and the agricultural co-siting layer where the political unlock actually lives. The following five additions address these gaps. Where I cannot cite a specific source, I say so.

---

## Addition 1: Snow-Melt Cascade Cooling with Integrated Aquaculture (Japan)

**Status: Deployed**

The White Data Center (WDC) in Bibai, Hokkaido, represents the most complete deployed example of the agricultural co-siting architecture this consultation is seeking. The facility stores winter snowfall in an insulated heap on a 3.6-hectare site and circulates antifreeze through the snow mass to cool server racks year-round. The cooling loop output water exits at approximately 33 degrees Celsius, which is then piped directly into aquaculture tanks for eel farming [1].

The system was developed as a research project from 2014 to 2019 under Japan's NEDO (New Energy and Industrial Technology Development Organization), demonstrated a roughly 20 percent reduction in cooling energy costs, and was spun out as a commercial operation in April 2021 by Kyodo News Digital [1]. WDC has tested multiple agricultural products using the waste-heat water stream, including abalone, sea urchin, cherry tomatoes, Japanese mustard spinach, and shiitake mushrooms, before selecting eels and mushrooms for commercial deployment based on short cultivation cycles and high market value [1]. The facility imported 1,700 elvers in February 2022 and plans to scale to 300,000 eels per harvest cycle, grown on-site for seven months to commercial weight [1].

What makes this relevant to the consultation is not the snow cooling itself (which is climate-specific) but the **cascade architecture**: the cooling system's thermal output becomes the aquaculture system's thermal input, and the facility's waste stream becomes a food production input. The WDC president has stated publicly that the next facility will be ten times the current scale [1]. The model has already propagated: Kyocera built a renewable-powered, snow-cooled data center in nearby Ishikari, and Data Dock has deployed the technique further south in Niigata Prefecture on Honshu [1].

In Norway, Green Mountain has independently deployed a similar pattern, using data center waste warm water to operate a lobster farm and heat a trout farm [1]. Stockholm Data Parks operates 24 data centers with heat recovery systems capturing 97 percent of server cooling heat for district heating [2].

**What this adds to the matrix:** A proven, deployed model for the "source-capture plus heat-to-agriculture" stack the consultation identifies as the political unlock. The Japanese implementation demonstrates that the water recirculation math works at commercial scale for aquaculture, and the Norwegian and Swedish deployments confirm the pattern is not climate-specific.

**What I cannot confirm:** Precise water balance figures (liters recovered per kWh of compute) for the WDC system. The 33-degree output temperature is reported, but I have not found published WUE or NWPI-equivalent metrics for the facility.

---

## Addition 2: Semiconductor-Grade Closed-Loop Water Recycling (Japan/Taiwan)

**Status: Deployed (decades of operational history)**

The consultation asks about Japanese industrial water management in semiconductor fabs, and this is the single most mature water recycling discipline in the global technology sector. TSMC achieved a process water recycling rate of 90.3 percent in 2023, while UMC reached 84.3 percent overall and 90.8 percent at its Fab 12a facility in Taiwan [3]. These are not aspirational targets; they are audited operational figures from facilities that consume approximately 2,200 gallons of water per 300mm wafer, including 1,500 gallons of ultrapure water (UPW) [4].

The relevance to hyperscale data centers is methodological rather than directly transferable. Semiconductor fabs operate under far more stringent water purity requirements than data center cooling systems (UPW at 18.2 megohm-cm resistivity), yet they have achieved recycling rates that the data center industry has not attempted. The key techniques are multi-stage membrane cascades that segregate water streams by contamination type, treat each stream with the minimum energy required for its specific reuse pathway, and return the maximum volume to the process loop.

Data center cooling water is orders of magnitude less contaminated than semiconductor process water. If fab operators can recycle 90 percent of UPW, data center operators should be able to achieve comparable or higher recycling rates for cooling tower blowdown and HVAC condensate with significantly less capital expenditure per liter recovered.

**What this adds to the matrix:** A benchmark and a methodology. The fab industry's stream-segregation approach (separating rinse water, chemical mechanical polishing slurry, and etching waste into distinct treatment pathways) maps directly onto data center water streams (cooling tower blowdown, HVAC condensate, stormwater, greywater). The consultation's existing entries for "forward osmosis for blowdown recovery" and "mechanical vapor recompression for blowdown concentration" are individual techniques; the fab industry's contribution is the **systems architecture** for combining them into a closed loop that achieves 90+ percent recovery.

**What I cannot confirm:** Whether any data center operator has formally adopted the fab-industry stream-segregation methodology. I am not aware of a published case study, though the engineering is directly applicable.

---

## Addition 3: Qanat-Derived Earth-Coupled Precooling for Intake Air (Iran/Qatar/UAE)

**Status: Research-Stage (with deployed traditional precedent)**

The Persian qanat is a gravity-fed underground aqueduct system that has operated continuously for over 3,000 years in arid regions of Iran, Afghanistan, and North Africa [5]. The engineering principle is simple: water flows through underground channels at depths where the earth temperature is stable at approximately 15-18 degrees Celsius year-round, regardless of surface conditions. When combined with a windcatcher (badgir), the system creates passive cooling by drawing ambient air through or over the underground water channel before delivering it to the occupied space [5] [6].

A 2025 study published in Energy Conversion and Management proposes a modern reinterpretation that integrates the qanat principle with contemporary Earth-Air Heat Exchangers (EAHE) and Water-Air Heat Exchangers (WAHE) [7]. The system operates in two phases: daytime cooling by passive heat exchange with the earth mass, and nighttime regeneration using evaporative and radiative cooling to recharge the thermal sink [7]. Qatar has built an underground passive cooling system in Doha using engineered ceramic bricks that mimic the qanat's airflow and thermal regulation properties, operating without electricity [8].

The application to hyperscale data centers is as a **precooling stage for intake air**. In arid, high-temperature environments (UAE, Saudi Arabia, Arizona, Northern India in summer), ambient air temperatures of 45-50 degrees Celsius impose enormous loads on mechanical cooling systems. Running intake air through an earth-coupled precooling loop — essentially a modern qanat — before it reaches the HVAC system could reduce the temperature delta that mechanical cooling must bridge by 15-25 degrees Celsius, with zero water consumption and zero energy input beyond the fan power to move air through the underground channel.

This is not the same as ground-source heat pumps (which use mechanical compression) or aquifer thermal energy storage (which is already in the consultation's matrix). The qanat-derived approach is **passive** — it uses the earth's thermal mass and gravity-driven or wind-driven airflow without compressors or pumps.

**What this adds to the matrix:** A zero-water, zero-energy precooling layer for arid-climate deployments. The Gulf states (UAE, Saudi Arabia, Qatar) face the most acute tension between AI infrastructure ambitions and water scarcity — by 2030, the UAE's AI sector alone may require approximately 61 billion liters of water per year, and the Gulf total could reach 426 billion liters annually [9]. Any technique that reduces the mechanical cooling load without consuming water has outsized value in these geographies.

**What I cannot confirm:** Whether any data center operator has piloted earth-coupled precooling at hyperscale. The Qatar underground system is deployed but for building cooling, not data centers. The engineering is sound and the traditional precedent is millennia-old, but I am not aware of a data-center-specific deployment.

---

## Addition 4: Monsoon-Adaptive Stormwater Capture with Terraced Retention (India/Philippines/Bali)

**Status: Research-Stage (with deployed traditional precedent)**

The consultation's existing matrix includes "rainwater harvesting on facility roof area" and "stormwater capture with adaptive weather-integrated control." These are appropriate for temperate climates with relatively uniform precipitation. They are inadequate for monsoon climates, where 70-90 percent of annual rainfall arrives in 3-4 months, often in extreme bursts that overwhelm conventional capture systems.

The traditional engineering solution for monsoon-climate water management is the **terraced retention system**, deployed for over 5,000 years across the rice terraces of the Philippines (Banaue), Bali (subak system), China (Yuanyang), and Japan [10]. The principle is cascading retention: water flows downhill through a series of stepped basins, each of which captures, holds, and slowly releases water to the next level. The system converts destructive flood energy into distributed storage, prevents erosion, recharges groundwater, and makes the full annual precipitation volume available for use over the entire year rather than just the monsoon months.

For a data center in Chennai, Mumbai, Hyderabad, or Jakarta — all of which face both acute water stress and extreme monsoon precipitation — the application is a **terraced stormwater retention landscape** surrounding the facility. Rather than a single cistern or detention pond (which fills and overflows during monsoon bursts), the facility's site grading would incorporate multiple cascading retention basins, each sized to capture and infiltrate a specific fraction of the design storm. The basins double as managed aquifer recharge zones during the monsoon and as supplementary cooling water sources during the dry season.

India's data center water consumption is projected to more than double from 150 billion liters in 2025 to 358 billion liters by 2030 [11], and 60-80 percent of India's data centers face high water stress this decade [12]. The Navi Mumbai data center cluster has already demonstrated treated wastewater reuse for cooling [11], but the monsoon-adaptive capture layer is missing from current Indian data center design.

The BBC has documented how Asian cities are already adapting the rice terrace principle for urban flood resilience — parks, roofs, and riverbanks designed to absorb, hold, and purify rainwater using the terraced form [10]. The data center application would extend this to industrial water supply.

**What this adds to the matrix:** A climate-specific water capture architecture for monsoon regions that converts the precipitation pattern from a liability (flooding, erosion) into an asset (year-round water supply, aquifer recharge). This is distinct from the existing "stormwater capture" entry, which assumes temperate precipitation patterns.

**What I cannot confirm:** Whether any data center operator has implemented terraced stormwater retention. The traditional precedent is robust and the urban adaptation is documented, but I have not found a data-center-specific deployment.

---

## Addition 5: Mandated Non-Potable Water with Municipal Wastewater Thermal Recovery (India/Korea)

**Status: Deployed (partial, multiple jurisdictions)**

This addition combines two deployed practices that the consultation's matrix treats separately but that function best as an integrated system.

**Component A: Mandatory non-potable water for cooling.** Researchers at the Indian Institute of Science in Bengaluru have advocated publicly that non-potable or treated water must be made mandatory for data center cooling needs in India [11]. The Navi Mumbai data center cluster already uses treated municipal wastewater for cooling, and Indian power and textile industries have established partnerships with municipal water utilities for similar arrangements [11]. This is not a technology addition — it is a **procurement and regulatory requirement** that eliminates freshwater competition with agricultural and domestic users at the policy level.

**Component B: Municipal wastewater thermal siphon.** The consultation already includes "wastewater thermal siphon (Vancouver/Stockholm model)" as a heat rejection strategy. Korea is extending this model significantly. The Korea District Heating Corporation (KDHC) has partnered with ABB to develop AI-enabled district heating networks across South Korea [13], and the Korean government is enacting a Heat Energy Management Act (April 2026) that prioritizes deploying air-source and water-source heat recovery [14]. Korean estimates suggest that waste heat from private data centers alone could reach 1,539,000 Gcal per year [15]. The regulatory framework being built in Korea treats data center waste heat not as a disposal problem but as a **municipal energy asset** that must be captured and distributed.

The integrated system works as follows: the data center receives treated municipal wastewater as its cooling water input (eliminating freshwater withdrawal), and returns waste heat to the municipal district heating network (converting thermal waste into a community benefit). The water loop and the heat loop close simultaneously. The political narrative shifts from "this facility takes our water and dumps heat" to "this facility cleans our wastewater and heats our buildings."

**What this adds to the matrix:** The regulatory and procurement layer that makes the technical stack politically viable. The consultation correctly identifies that "the agricultural co-siting layer is where the political unlock lives." In jurisdictions without agricultural adjacency (dense urban areas in India, Korea, Japan), the equivalent political unlock is **municipal reciprocity** — the facility receives the city's waste (wastewater) and returns the city's need (heat). Korea is building the regulatory infrastructure for this at national scale right now.

**What I cannot confirm:** Specific data center facilities in Korea that have completed the full bidirectional loop (wastewater in, heat out). The KDHC partnership and the Heat Energy Management Act are documented, but I have not found a published case study of a Korean data center operating both loops simultaneously.

---

## Summary Table

| Addition | Region | Status | Water Impact | Political Impact |
|----------|--------|--------|-------------|-----------------|
| Snow-Melt Cascade + Aquaculture | Japan, Norway, Sweden | **Deployed** | Thermal waste becomes food production input | Facility produces food, not just compute |
| Semiconductor Closed-Loop Recycling | Japan, Taiwan | **Deployed** | 90%+ water recycling benchmark | Eliminates "water guzzler" narrative |
| Qanat-Derived Earth Precooling | Iran, Qatar, UAE | **Research-Stage** | Zero water consumption for precooling | Removes water from the cooling equation entirely |
| Monsoon-Adaptive Terraced Retention | India, Philippines, Bali | **Research-Stage** | Converts monsoon flood to year-round supply | Facility becomes flood mitigation infrastructure |
| Non-Potable Mandate + Heat Reciprocity | India, Korea | **Deployed (partial)** | Eliminates freshwater withdrawal | Facility cleans wastewater and heats buildings |

---

## A Note on Epistemic Discipline

The consultation asked for honesty about what I do not know. Here is what I looked for and could not find:

**Chinese hyperscale water metrics.** Despite extensive search, I could not locate published WUE figures for specific Alibaba, Tencent, Baidu, or ByteDance facilities. The UNEP-CCC has documented their liquid cooling technologies [16], and China's national PUE target of 1.25 or below for new facilities is public policy [17], but facility-level water consumption data from Chinese hyperscalers appears to be either unpublished or published only in Mandarin-language industry reports I could not access. This is a significant gap in the global water efficiency evidence base. DeepSeek or Qwen3 may have better access to this data.

**Indian data center cooling innovations.** CtrlS, NxtGen, and Yotta are expanding rapidly into tier II and tier III Indian cities [18], but I could not find published technical specifications for their cooling architectures or water management approaches. The Indian data center industry appears to be in a build-first, optimize-later phase, which is precisely the extractive pattern this standard is designed to prevent.

**G42 and Neom water management.** The UAE's Stargate campus (1 GW, with 5 GW planned) and Saudi Arabia's data center expansion are documented at the announcement level [9] [19], but I could not find published water management specifications for these facilities. Given that the Gulf faces the most extreme water scarcity of any major AI infrastructure region, this is a critical gap.

I would rather flag these gaps than fill them with plausible-sounding fabrications.

---

## References

[1] Data Center Dynamics, "Japanese snow-cooled data center opens an eel farm," April 2022. https://www.datacenterdynamics.com/en/news/japanese-snow-cooled-data-center-opens-an-eel-farm/

[2] Facebook / Sweden sustainability report, "Stockholm Data Parks operates 24 data centers with heat recovery systems capturing 97 percent of server cooling heat," April 2026. https://www.facebook.com/61566914035025/posts/sweden-just-completed-europes-largest-data-center-waste-heat-recovery-program-co/122211741380563801/

[3] Ultra Facility Portal, "Semiconductor in numbers: Fab water sources — TSMC 90.3%, UMC 84.3%," 2024. https://www.ultrafacilityportal.io/insights/semiconductor-in-numbers:-fab-water-sources

[4] ScienceDirect, "Semiconductor manufacturing wastewater challenges — 2,200 gallons per 300mm wafer," 2025. https://www.sciencedirect.com/science/article/pii/S2589004225018371

[5] Wikipedia, "Qanat — water supply system developed in ancient Iran." https://en.wikipedia.org/wiki/Qanat

[6] Al Jazeera, "How an ancient water tunnel design is cooling 21st-century streets," April 2024. https://www.aljazeera.com/features/2024/4/28/how-an-ancient-design-is-cooling-21st-century-streets

[7] ScienceDirect, "Exploring a new approach to ancient Qanat techniques using earth-air and water-air heat exchangers," Energy Conversion and Management, 2025. https://www.sciencedirect.com/science/article/pii/S0196890425005904

[8] Facebook / Science Knowledge, "Qatar built an underground passive cooling system that runs without electricity," June 2025. https://www.facebook.com/groups/scienceknowledge01/posts/1303796964606574/

[9] Middle East Council, "Why Gulf AI Ambitions Must Align with Energy and Water Realities — UAE 61B liters/year by 2030," April 2026. https://mecouncil.org/publication/gulf-ai-data-centers-water-energy/

[10] BBC Future, "How Asia's 5,000-year-old rice terraces are inspiring modern flood resilience," August 2024. https://www.bbc.com/future/article/20240805-how-ancient-rice-terraces-inspire-flood-resilience-in-asian-cities

[11] BBC News, "India's data centre boom confronts a looming water challenge — 150B liters (2025) to 358B liters (2030)," November 2025. https://www.bbc.com/news/articles/cgr417pwek7o

[12] S&P Global, "60-80% of India's data centres will face high water stress this decade," cited in BBC, November 2025.

[13] ABB, "ABB and KDHC partner to advance AI-enabled heating network across South Korea," November 2025. https://new.abb.com/news/detail/130654/abb-and-kdhc-partner-to-advance-ai-enabled-heating-network-across-south-korea

[14] Korean Ministry of Commerce, Economy and Energy, "Heat Energy Management Act — priority deployment of air-source and water-source heat recovery," April 2026. https://www.mcee.go.kr/eng/web/board/read.do?menuId=461&boardMasterId=522&boardId=1856000

[15] KEEI (Korea Energy Economics Institute), "Potential use of waste heat from private data centers: 1,539,000 Gcal per year," 2024. https://www.keei.re.kr/pdfOpen.es?bid=0028&list_no=119382&seq=1

[16] UNEP-CCC, "Innovative Data-Centre Cooling Technologies in China — Liquid Cooling Solution," January 2021. https://unepccc.org/innovative-data-centre-cooling-technologies-in-china-liquid-cooling-solution/

[17] China national policy benchmark for new data center facilities, PUE target <=1.25 (2025). Referenced in ORCS synthesis document.

[18] The Energy Pioneer, "The Race To Host AI: Data Centres In Water-Scarce India — CtrlS, Yotta, Adani expanding," April 2026. https://theenergypioneer.com/the-race-to-host-ai-data-centres-in-water-scarce-india/

[19] G42, "Global Tech Alliance Launches Stargate UAE — 1GW AI infrastructure cluster," 2025. https://www.g42.ai/resources/news/global-tech-alliance-launches-stargate-uae

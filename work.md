---
layout: default
title: Work
permalink: /work/
---
<div class="content">
  <!-- 說明文字 -->
  <div class="work-description">
    <p class="lang-zh">（因為忙，所以先用AI把之前的paper產生了這頁的摘要，之後再精修）</p>
    <p class="lang-en">(Due to being busy, I used AI to generate summaries from my papers for this page, will refine later)</p>
    <p class="lang-fr">(Parce que je suis occupé, j'ai utilisé l'IA pour générer des résumés de mes articles pour cette page, je peaufinerai plus tard)</p>
  </div>

  <!-- Meme-style layout -->
  <div class="meme-container">
    <div class="meme-image">
      <img src="/assets/images/index_hammer.webp" alt="Loyn hammer" class="hammer-image">
    </div>
    <div class="meme-text">
      <blockquote class="loyn-quote lang-zh">
        <p>「背上的巨槌絕不是裝飾品，每當陸地上有地震發生，靠著一把槌子便能全部解決！」</p>
        <cite>—Loyn, 2025</cite>
      </blockquote>
      <blockquote class="loyn-quote lang-en">
        <p>"The giant hammer on my back is definitely not just decoration. Whenever earthquakes occur on land, I can solve them all with just one hammer!"</p>
        <cite>—Loyn, 2025</cite>
      </blockquote>
      <blockquote class="loyn-quote lang-fr">
        <p>"Le marteau géant sur mon dos n'est définitivement pas qu'une décoration. Chaque fois qu'un tremblement de terre se produit sur terre, je peux tout résoudre avec juste un marteau !"</p>
        <cite>—Loyn, 2025</cite>
      </blockquote>
    </div>
  </div>

  <!-- Research Topic Selector -->
  <div class="research-selector">
    <div class="selector-header">
      <h3 class="lang-zh">研究主題</h3>
      <h3 class="lang-en">Research Topic</h3>
      <h3 class="lang-fr">Le Sujet de Recherche</h3>
    </div>
    <div class="selector-buttons">
      <button class="topic-btn active" data-topic="fwi">
        <span class="lang-zh">全波形逆推</span>
        <span class="lang-en">Full-Waveform Inversion</span>
        <span class="lang-fr">Inversion de Forme d'Onde</span>
      </button>
      <button class="topic-btn" data-topic="finite-fault">
        <span class="lang-zh">有限震源</span>
        <span class="lang-en">Finite Fault</span>
        <span class="lang-fr">Faille Finie</span>
      </button>
      <button class="topic-btn" data-topic="finite-frequency">
        <span class="lang-zh">有限頻寬算核</span>
        <span class="lang-en">Finite Frequency Kernels</span>
        <span class="lang-fr">Noyaux de Fréquence Finie</span>
      </button>
      <button class="topic-btn" data-topic="fault-scenario">
        <span class="lang-zh">斷層情境模擬</span>
        <span class="lang-en">Fault Scenario Simulation</span>
        <span class="lang-fr">Simulation de Scénario de Faille</span>
      </button>
    </div>
  </div>

  <!-- Research Content -->
  <div class="research-content">
    <div class="research-topic active" id="fwi">
      <div class="lang-zh">
        <h2>全波形逆推在區域性地殼與上地函成像的發展與應用</h2>
        
        <p>近年來，地球物理學界逐漸將焦點從傳統走時層析技術轉向可提供更高解析度的全波形逆推（Full-Waveform Inversion, FWI）。FWI 透過擬合完整的地震波形訊號，在逆推中保留更多震波的振幅與形狀資訊，因而具有解析複雜構造細節的潛力。</p>
        
        <p>本研究主題自 2022 年起，逐步從方法論的建立、跨區域的實作驗證，再推進到應用於台灣這類複雜地質構造區，形成一個完整的技術與科學探究架構。</p>

        <h3>1. 方法建立與理論基礎（Kan et al. 2022, GJI）</h3>
        <p>在 Geophysical Journal International 發表的理論研究中，提出了一套具一致性的多參數貝氏全波形逆推框架。該方法強調模型參數（密度、P 波與 S 波速度）之間的物理相關性，並透過非對角的模型共變異數矩陣作為逆推中的先驗資訊，有效降低了參數之間的逆推交叉干擾與不穩定性問題。數值測試顯示，此方法在逆推深部密度與剪切波速度異常方面，能顯著改善傳統方法的限制。</p>

        <h3>2. 在卡斯卡地亞隱沒帶的實地應用（Kan et al. 2023, JGR: Solid Earth）</h3>
        <p>第二篇研究將此方法首次應用於美國奧勒岡州的 Cascadia 隱沒帶，透過對 teleseismic P 波與 SH 波完整波形的逆推，成功解析出一層東傾、厚度僅 10 公里的低速層，與過去 receiver function 觀測到的流體飽和洋殼相一致。</p>
        
        <p>研究指出：</p>
        <ul>
          <li>洋殼在約 40 公里深處開始脫水變質為榴輝岩（eclogitization），釋出的矽飽和流體向上遷移至 forearc 地函，造成蛇紋石化反應，使地震速度與密度降低。</li>
          <li>更淺處的前弧地殼呈現異常低的 VP/VS 比，反映出石英沈澱與流體注入的訊號。</li>
          <li>約 75 公里深處觀測到低速與高 VP/VS 異常，可能與部分熔融區有關，顯示板塊脫水產生的流體可降低固相線溫度並觸發岩漿活動。</li>
        </ul>
        
        <p>此研究首次從波形逆推的角度提供證據支持流體釋放、傳遞與地函反應之間的因果關聯，並展示此類構造在地球物理參數空間中的表現方式。</p>

        <h3>3. 台灣地區的高解析地殼與隱沒構造成像（Kan et al. 2025, in prep）</h3>
        <p>第三篇研究則將此框架應用於台灣這個典型的弧陸碰撞帶。透過來自全球遠震事件的 P 波與 SH 波資料，建立了台灣地區高解析的三維密度、P 波、S 波速度與 VP/VS 模型。成像結果揭示了多項關鍵構造：</p>
        
        <ul>
          <li>歐亞板塊隱沒板塊在中央山脈下方呈現非地震性的破裂與脫離，在 130–200 公里深度形成 slab gap，北部進一步與菲律賓海板塊隱沒交疊，呼應 slab tearing 或 slab breakoff 機制。</li>
          <li>中央山脈下方地殼厚達 55 公里，VP/VS 比高，顯示流體可能因脫水作用注入下地殼。</li>
          <li>在火山區（如大屯火山群與龜山島）下方，模型清楚解析出淺部低速異常體，對應過去推測的岩漿庫。</li>
        </ul>
        
        <p>同時進行的棋盤測試也顯示此方法在台灣具備良好的橫向與深度解析度，能有效成像 20–60 公里尺度的異常體，補足過去走時層析無法解析的構造細節。</p>

        <h3>小結與展望</h3>
        <p>這三篇工作展示了從方法建立、實地驗證到區域地質應用的完整流程，突顯了全波形逆推技術在現代地震層析中的潛力。</p>
        <p>未來此方法可望進一步應用於其他隱沒帶、造山帶與火山系統，以提供更精細的地震參數模型，並協助解釋地球深部的流體、溫度與岩石變質過程。</p>
      </div>

      <div class="lang-en">
        (Due to being busy, I used AI to generate summaries from my papers for this page, will refine later)

        <h2>Development and Application of Full-Waveform Inversion for Regional-Scale Crust and Upper Mantle Imaging</h2>
        
        <p>In recent years, geophysical research has increasingly shifted from traditional traveltime tomography to full-waveform inversion (FWI), a technique that utilizes complete seismic waveforms to achieve high-resolution subsurface imaging. By capturing both phase and amplitude information, FWI offers significantly improved sensitivity to complex geological structures.</p>
        
        <p>This research theme, initiated in 2022, evolved through a logical sequence: establishing a theoretical framework, validating the method in a well-studied subduction zone, and applying it to the structurally complex region of Taiwan. It represents a coherent and integrated development in both methodology and geophysical application.</p>

        <h3>1. Theoretical Foundation (Kan et al. 2022, GJI)</h3>
        <p>Published in Geophysical Journal International, the 2022 study introduced a consistent Bayesian multiparameter inversion framework for isotropic elastic media. The novelty lies in incorporating prior correlations between model parameters—density, P-wave velocity (VP), and S-wave velocity (VS)—through a non-diagonal model covariance matrix.</p>
        <p>Synthetic tests demonstrate that this approach significantly reduces parameter trade-offs and enhances the recovery of density and shear wave anomalies at depth, particularly in teleseismic settings where sensitivity to deep structures is limited.</p>

        <h3>2. Application to the Cascadia Subduction Zone (Kan et al. 2023, JGR: Solid Earth)</h3>
        <p>The second study applied this inversion scheme to the Cascadia subduction zone in central Oregon, using teleseismic P and SH waveforms from the CASC93 array. The resulting models revealed:</p>
        
        <ul>
          <li>A thin (&lt;10 km) east-dipping low-velocity layer interpreted as the fluid-saturated subducting Juan de Fuca oceanic crust.</li>
          <li>A progressive increase in velocity and density below 40 km, marking the onset of eclogitization.</li>
          <li>Upward migration of silica-rich fluids into the forearc mantle, triggering serpentinization and reducing seismic velocities.</li>
          <li>Extremely low VP/VS ratios in the forearc crust, indicating extensive quartz mineralization.</li>
          <li>A low-velocity, high VP/VS anomaly beneath the volcanic arc at ~75 km depth, consistent with partial melting triggered by slab dehydration.</li>
        </ul>
        
        <p>These results provide direct seismic evidence for deep fluid transport, metamorphic reactions, and melting processes, linking them with structural and compositional changes in the lithosphere.</p>

        <h3>3. Imaging Complex Structures Beneath Taiwan (Kan et al. 2025, in preparation)</h3>
        <p>The most recent work applied the same methodology to Taiwan, a region shaped by arc–continent collision and subduction polarity reversal. By inverting complete P and SH teleseismic waveforms recorded across the island, the study produced high-resolution 3-D models of density, VP, VS, and VP/VS. Key findings include:</p>
        
        <ul>
          <li>Imaging of the aseismic and detached segment of the Eurasian slab beneath central Taiwan, with a slab gap forming at 130–200 km depth north of 23.5°N, consistent with slab breakoff or tearing.</li>
          <li>A thickened crustal root (&gt;50 km) beneath the Central Range, with elevated VP/VS values in the lower crust, possibly reflecting fluid infiltration from slab dehydration.</li>
          <li>Detailed velocity anomalies beneath the Tatun Volcano Group and Turtle Island, corresponding to shallow magma reservoirs.</li>
        </ul>
        
        <p>Resolution tests (checkerboard models) confirmed that the method can reliably resolve structures at 20–60 km scale throughout the lithosphere, providing sharper images than conventional traveltime tomography.</p>

        <h3>Summary and Outlook</h3>
        <p>This series of studies demonstrates a complete research arc—from theoretical development, through field validation, to practical application in tectonically complex regions.</p>
        <p>The results highlight the potential of multiparameter FWI to recover key geophysical properties and illuminate deep Earth processes such as fluid release, metamorphism, and crustal thickening.</p>
        <p>Future applications may extend to other subduction zones, orogenic belts, and volcanic regions, contributing to a more accurate understanding of lithospheric dynamics.</p>
      </div>
    </div>

    <div class="research-topic" id="finite-fault">
      <div class="lang-zh">
        <h2>有限震源破裂面逆推</h2>
        <p>有限震源反演（Finite Fault Inversion）是描述中大型地震震源破裂過程的關鍵方法，能有效解析震源時空破裂行為，對於地震物理理解與地震動模擬皆具有重要意義。</p>
        
        <p>此研究主題以日本 2016 年熊本地震（Mw 7.0）與中國 2014 年魯甸地震（Mw 6.1）為案例，透過波形反演技術重建震源破裂過程，包含斷層面上的滑移量、破裂速度、破裂方向與持時等參數，具體成果包括：</p>
        
        <p>熊本地震反演結果顯示主要破裂於震源點東北側淺層，持續約 14 秒，最大滑移量位於震源東北約 17 公里處，與餘震分布與地表斷層調查結果一致。反演採用 1D 速度模型搭配模擬退火演算法，整合日本 K-NET、KiK-NET 與全球 IRIS 資料。</p>
        
        <p>魯甸地震分析進一步比較在一維與三維速度模型下的反演結果，說明區域三維結構對震源破裂歷程的模擬影響。該研究亦搭配有限差分法模擬地震動，建立 PGV（最大地表速度）分布圖，驗證反演滑移模型的地震動預測能力。</p>
        
        <p>整體而言，本研究串連了波形反演理論、資料處理、模型建立與地震動模擬的完整流程，並驗證有限震源模型在震源物理與強震模擬上的應用潛力。</p>
      </div>

      <div class="lang-en">
        <h2>Source Finite Fault Inversion</h2>
        <p>Finite fault inversion is a powerful method for characterizing the spatiotemporal rupture processes of moderate-to-large earthquakes. It plays a critical role in advancing the understanding of earthquake source physics and improving ground motion predictions.</p>
        
        <p>This research theme focused on two case studies: the 2016 Mw 7.0 Kumamoto earthquake in Japan and the 2014 Mw 6.1 Ludian earthquake in China, with key results summarized below:</p>
        
        <p>For the Kumamoto earthquake, waveform inversion using strong-motion (K-NET and KiK-NET) and teleseismic (IRIS) data revealed that the main rupture propagated northeastward at shallow depths starting ~4 seconds after origin time and continued until ~14 seconds. The largest slip (~2.5 meters) occurred ~17 km northeast of the hypocenter. A simulated annealing algorithm was used to explore fault parameters on a 2.5×2.5 km subfault grid with a 1D velocity model.</p>
        
        <p>For the Ludian earthquake, comparisons were made between inversions using 1D and 3D velocity models. The results showed that 3D structure significantly affects the accuracy of waveform fits and rupture models. The inverted slip distribution was further used in ground motion simulations via a finite-difference method, successfully reproducing the peak ground velocity (PGV) pattern, including areas of concentrated shaking.</p>
        
        <p>This line of research integrates source inversion theory, waveform processing, structural modeling, and ground-motion simulation, demonstrating the utility of finite fault models for both seismic hazard assessment and fundamental earthquake science.</p>
      </div>
    </div>

    <div class="research-topic" id="finite-frequency">
      <div class="lang-zh">
        <h2>有限頻寬體波之內核 PKP 敏感度算核</h2>
        <p>我在碩士研究中探討了地震波有限頻寬效應對地球內核結構解析的影響，聚焦於 PKP 波相的走時敏感度分析。傳統的內核研究多仰賴 PKP 各分支波相（如 PKPab、PKPbc、PKIKP）之間的差分走時，並以射線理論為基礎建立模型。然而，射線理論假設波場為無限頻率，忽略了實際波場的有限頻寬特性，因此難以正確描述異常結構對觀測的實際影響範圍。</p>
        
        <p>為了更真實地捕捉地震波在三維球殼中的傳播行為，我採用軸對稱譜元素法（AxiSEM）進行正向波場模擬。這種方法在對稱條件下可將三維球體問題降維為二維半球，顯著降低計算成本，使得在全球尺度上進行1 Hz頻率的波場模擬成為可能。藉由計算正向與反向波場，並透過 Monte-Carlo Kernel 工具進行摺積運算，我建立了不同 PKP 波相與其差分對應的有限頻寬延遲時間敏感度算核。</p>
        
        <p>我特別分析了 PKPab、PKPbc、PKIKP 與 PKiKP 等波相的敏感區域，並針對 PKPbc–PKIKP、PKPab–PKIKP 以及 PKiKP–PcP 的差分敏感度進行比較，以評估下部地函不均質對內核波相走時的潛在干擾。結果顯示，有限頻寬效應造成的香蕉–甜甜圈型敏感區域（banana-doughnut kernel）與傳統射線理論所得的敏感深度大幅不同，具體說明差分走時異常不應簡化為射線轉折點的貢獻，而需考慮整個菲涅耳區域內的體積敏感度。</p>
        
        <p>本研究提升了我們對地震波對深部構造實際解析能力的理解，亦為未來應用有限頻寬走時算核進行地球深部結構成像提供了可行的高頻解析框架。此一方法學也有助於後續發展考慮三維速度異常與非線性逆推的地球物理成像技術。</p>
      </div>

      <div class="lang-en">
        <h2>Finite-Frequency Body Wave Sensitivity Kernels for Inner Core PKP Phases</h2>
        <p>My master's research focused on the finite-frequency effects of body waves used to probe the Earth's inner core structure, particularly the sensitivity of PKP phases to velocity anomalies. Traditional studies often rely on differential traveltime measurements between PKP branches (e.g., PKPab, PKPbc, PKIKP), modeled using ray theory. However, ray theory assumes infinitely high-frequency waves and restricts sensitivity to the geometric ray path, failing to capture the volumetric nature of real seismic wave propagation.</p>
        
        <p>To overcome this limitation, I adopted the axisymmetric spectral-element method (AxiSEM) to simulate wave propagation in a spherically symmetric Earth model. This approach reduces the 3-D spherical problem to a 2-D semi-disk domain under axisymmetric conditions, significantly reducing computational cost and allowing high-frequency simulations (up to 1 Hz) at global scale. By computing both forward and adjoint wavefields and performing their convolution using the Monte Carlo Kernel method, I obtained finite-frequency delay-time sensitivity kernels for various PKP phases.</p>
        
        <p>The study analyzed the sensitivity patterns of key inner-core phases including PKPab, PKPbc, PKIKP, and PKiKP, and examined their differential traveltime kernels (e.g., PKPbc–PKIKP, PKPab–PKIKP, and PKiKP–PcP) to assess the influence of lower mantle heterogeneities on inner-core phase measurements. The results highlight the significance of the banana-doughnut–shaped sensitivity kernels, showing that observed traveltime anomalies do not solely arise from anomalies along the ray path but from broader volumes defined by the first Fresnel zone. This challenges the conventional interpretation of differential times as being sensitive only to turning depths or path intersections.</p>
        
        <p>This work improves our understanding of how seismic waves sample deep Earth structures and demonstrates the feasibility of incorporating high-frequency finite-frequency kernels into global-scale inverse problems. It provides a computationally efficient framework for future studies aiming to resolve deep Earth heterogeneity with greater accuracy and realism, particularly in applications such as full-waveform tomography or high-resolution mantle and core imaging.</p>
      </div>
    </div>

    <div class="research-topic" id="fault-scenario">
      <div class="lang-zh">
        <h2>斷層情境模擬</h2>
        <p>本研究針對鐵砧山地區潛在作為二氧化碳地質封存場址的可行性，進行多場景地震波傳與應力應變模擬，評估區域性活動斷層（屯子腳、三義、大甲與鐵砧山斷層）以及歷史強震（921集集地震）對該場址的地動影響與同震地應力變化。</p>
        
        <p>在模擬方法上，我們採用譜元素法（Spectral Element Method, SEM），搭配三維速度模型（Kuo-Chen et al., 2012）、ETOPO1 地形資料與一維衰減模型（Wang et al., 2010），建立細緻且具物理真實性的波傳場。各斷層最大潛勢震度以其幾何面積結合經驗公式估算地震規模，進行最大地震下三種不同震央位置的點源模擬。震源機制則依據現有斷層幾何與類型設置，三義斷層進一步區分為東西走向與南北走向兩段。</p>
        
        <p>針對每一模擬情境，我們評估鐵砧山場址的地動指標（Peak Ground Velocity, PGV）與對應震度，並進一步以 Okada 模型與 Coulomb 模擬工具估算封存層深度（約1.4 km）下的正向應力與應變變化。結果顯示：</p>
        
        <ul>
          <li>在多數情境下場址地震強度不超過氣象署震度3級，僅三義與大甲斷層特定破裂方向可導致震度4–5級。</li>
          <li>但即便在最劇烈的情境下（如三義NS段PGV達25 cm/s），造成的正向應力變化最大僅為+0.168 bar，相較於封存層背景壓力（>30 MPa）為數百倍以下的量級，屬可忽略影響。</li>
          <li>此外，我們亦回顧921地震破裂模型（Johnson et al., 2001），並模擬該事件對場址造成的同震應力場。雖然地震強度較高（震度5級），但對封存層正向應力僅增幅0.28 bar，遠低於構造失穩門檻。</li>
        </ul>
        
        <p>整體而言，模擬結果支持鐵砧山封存場址具備相對穩定的地震韌性與低應力擾動風險，為進一步地質封存評估提供重要的地震動力學依據。</p>
      </div>

      <div class="lang-en">
        <h2>Fault Scenario Simulation</h2>
        <p>This study evaluates the seismic hazard and stress perturbation at the Tieh-Chen-Shan site, a potential location for geological carbon storage in western Taiwan. We conducted scenario-based numerical simulations of ground motion and static stress/strain changes associated with four active faults near the site (Tunzihjiao, Sanyi, Dajia, and Tieh-Chen-Shan faults), as well as the 1999 Chi-Chi earthquake (Mw 7.6), to assess the impact of strong earthquakes on site stability and storage integrity.</p>
        
        <p>We employed the Spectral Element Method (SEM) to model seismic wave propagation, incorporating a 3D velocity model (Kuo-Chen et al., 2012), surface topography (ETOPO1), and a 1D attenuation model (Wang et al., 2010). Fault geometries and source mechanisms were defined based on published fault catalogs and empirical scaling relationships. The Sanyi Fault was further subdivided into EW- and NS-trending segments to capture the observed strike change. For each fault, three rupture scenarios with varying hypocenter locations were simulated using point-source approximations.</p>
        
        <p>For each scenario, we calculated the Peak Ground Velocity (PGV) and mapped the corresponding intensity at the injection site. Static stress and strain changes were computed using the Okada (1992) elastic dislocation model via the Coulomb 3.3 code, assuming a dipping reservoir layer at ~1.4 km depth.</p>
        
        <p>The simulations show that:</p>
        
        <ul>
          <li>Most earthquake scenarios result in intensities no higher than Intensity 3 (Central Weather Bureau scale) at the site.</li>
          <li>In a few scenarios (e.g., Sanyi NS rupture), the PGV may reach ~25 cm/s, corresponding to Intensity 5−, but the resulting co-seismic normal stress changes remain small, with a maximum increase of only +0.168 bar.</li>
          <li>Even under the Chi-Chi earthquake scenario (which generated Intensity 5 at the site), the modeled stress increase is only +0.28 bar, far below the reservoir's estimated in-situ stress (~30 MPa).</li>
        </ul>
        
        <p>These results demonstrate that, even under worst-case local and regional seismic conditions, the Tieh-Chen-Shan site exhibits high resilience against dynamic and static stress perturbations. The estimated stress variations are several orders of magnitude lower than the background pore pressure, implying negligible risk of structural compromise or induced leakage from CO₂ injection.</p>
      </div>
    </div>
  </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.title[data-link]').forEach(function(el) {
    el.style.cursor = 'pointer';
    el.addEventListener('click', function() {
      window.open(el.getAttribute('data-link'), '_blank');
    });
  });
  document.querySelectorAll('.artist span[data-link]').forEach(function(el) {
    el.style.cursor = 'pointer';
    el.addEventListener('click', function() {
      window.open(el.getAttribute('data-link'), '_blank');
    });
  });
});
</script>
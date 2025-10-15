# Ontology of the Simulated Universe (OSIU) — Call for Collaborators
**Version:** v0.5 outreach package · **Lead:** Joshua Hickerson (Independent Researcher)  
**Focus:** Moral–informational dynamics, causal-loop cosmology, computational simulations

---

## 1) Purpose in One Paragraph
*OSIU* proposes a metaphysical architecture where physics, consciousness, and ethics are dual projections of structured information. Cosmology is modeled as a **closed causal loop** (torus topology), and morality is operationalized as **entropy management** via a moral gradient \(\mathcal{M}(t)\). v0.5 consolidates critiques by reframing equations as **testable dynamics**, adding a **Phenomenal Projection operator (Φ)** and a **Manifold Fitness function (Ω)**, and providing an **open simulation stack** to explore stability/collapse regimes.

---

## 2) What We’re Building (Now)
- **A lightweight simulation sandbox** (Python) that models \(\kappa,\sigma,\rho,\phi\) dynamics and computes \(\mathcal{M}(t)\) under shocks and interventions.
- **Data mapping layer**: practical proxies for the moral–informational variables against public datasets.
- **Falsifiable signatures** (correlational): stability vs. entropy flux; responsiveness vs. volatility; diversity vs. resilience.
- **Figures & explainers**: torus cosmology plates, captioned academic versions, and public-facing diagrams.

---

## 3) Roles We’re Seeking
- **Math & Theory** (1–2): Normalize/derive the placeholder ODEs; propose Lyapunov/free-energy functionals; analyze fixed points and stability.
- **Simulation Engineering** (1–2): Parameter sweeps, reproducibility, experiment registry; CI-ready notebooks.
- **Data & Empirics** (1–2): Proxy design, ETL, cleaning; basic statistics for correlation testing.
- **Visualization** (1): Publication-grade plots; interactive figures for public posts.
- **Philosophy Editor** (1): Short-form briefs for philosophers + public reviewers; terminology coherence.

> We welcome critical collaborators. The frame is metaphysical; the agenda is *empirical traction.*

---

## 4) Data Mapping: Variables → Proxies (First Pass)
Below are **starting proxies**; teams will refine and justify choices. This is to enable early correlational tests and sanity checks.

| Symbol | Concept | Measurement Idea | Candidate Public Sources (examples) |
|---|---|---|---|
| \(\kappa\) | Care / Cooperation | Prosociality, trust, giving, social support | World Values Survey (trust/helping), Gallup World Poll (helped a stranger, donated), World Giving Index |
| \(\sigma\) | Suffering / Instability | Conflict intensity, mortality/morbidity burden, disaster impact | UCDP/PRIO conflict datasets; WHO / IHME DALYs; EM-DAT disaster losses; ACLED events |
| \(\rho\) | Responsiveness (adaptive capacity) | Recovery time after shocks, fiscal/health response agility | OECD resilience indicators; World Bank governance effectiveness; disaster response time metrics |
| \(\phi\) | Pluralism (diversity tolerance) | Diversity + rights protection + polarization control | V-Dem liberal democracy index & civil liberties; Ethnic/linguistic fractionalization indices; religious diversity metrics |
| **Entropy proxy** | Structural stress/flux | Energy intensity, volatility, information throughput | Our World in Data energy intensity; econ volatility indices; mutual information on comms/network data (where available) |
| \(\mathcal{M}(t)\) | Moral Gradient | Computed: \(\frac{\kappa}{\sigma+\varepsilon}\,\rho\,\phi\) (normalized) | Derived from the above, normalized per unit time |
| **Intervention** | Crossing Minority | Minimal pulses when \(\sigma\) exceeds \(\sigma_{crit}\) | Policy events / treaty enactments / ceasefires; humanitarian surge episodes |

**Mapping Principles**
1. Prefer **transparent, widely-used datasets** with stable definitions.  
2. Keep each proxy **dimensionless or normalized** (z-scores or min–max per region/time).  
3. Document **assumptions and caveats** (e.g., DALYs ≠ all suffering).  
4. Publish a **variable dictionary** and **codebook** alongside CSVs.

---

## 5) Repo / OSF Structure
**Public OSF project components:**
```
/OSIU-v0.5
  /paper/                 # Whitepaper PDF, figures (torus)
  /simulation/            # Code: Universe model, sweeps, heatmaps
  /data/                  # Raw proxies (CSV) + README data dictionaries
  /results/               # Sweep CSVs, plots, notebooks
  /docs/                  # Briefs, slide decks, outreach letter
  /figures/               # Caption-embedded plates (PDF/PNG/SVG)
  /licenses/              # MIT (code), CC-BY (figures/text)
```
**GitHub mirror** recommended for code + issues. OSF remains the “source of truth” for datasets and releases.

---

## 6) Getting Started
1. **Clone or unzip** the starter: `osiu-sim-starter.zip`  
2. Install: `pip install -r requirements.txt`  
3. Run scenarios: `python -m simulation.experiments` (plots to `data/outputs/`)  
4. **Parameter sweep:**  
   ```bash
   python -m simulation.sweep --param phi --start 0.1 --end 1.0 --num 10
   python -m simulation.sweep2d --p1 phi --start1 0.1 --end1 1.0 --n1 12                                 --p2 a_s --start2 0.05 --end2 0.3 --n2 10                                 --shock poisson --out data/outputs/heat_phi_a_s
   ```
5. **Re-plot from CSV:**  
   ```bash
   python -m simulation.plot_csv --csv data/outputs/heat_phi_a_s.csv
   ```

---

## 7) Collaboration Norms
- Code: MIT. Text & figures: CC-BY 4.0.  
- PRs must include a short **“Assumptions & Limitations”** section.  
- Keep metaphysical claims **separate** from empirical testing code.  
- No hype: label placeholders clearly; pre-register risky tests when feasible.

---

## 8) Open Research Questions
- Can \(\rho\) (responsiveness) statistically predict reductions in entropy flux after shocks across 30–50 year windows?  
- Is there a robust inverted-U between \(\phi\) (pluralism) and stability that flattens in mature systems?  
- Do minimal **crossing minority** pulses out-perform constant interventions in simulations?  
- What Lyapunov/free-energy candidate tracks stability across regimes?

---

## 9) Contact & Participation
- **Project Lead:** Joshua Hickerson — *Ontology of the Simulated Universe Series*  
- **Interested?** Open an issue on the repo (GitHub mirror) or request OSF access.  
- **Email template:** “Interested in Data/Simulation/Math role for OSIU v0.5” with 2–3 sentences on your background.

---

### Appendix A — Variable Dictionary (to be expanded)
- **kappa**: [0,1], normalized cooperation/care (higher = more prosocial structure)  
- **sigma**: [0,1], normalized suffering/instability (higher = greater burden)  
- **rho**: [0,1], adaptive responsiveness (elasticity to shocks)  
- **phi**: [0,1], pluralism tolerance (diversity support without fragmentation)  
- **M(t)**: computed moral gradient; not bounded; used for stability comparisons  
- **shock(t)**: exogenous perturbations (Poisson bursts or Gaussian drift)

© Joshua Hickerson — Ontology of the Simulated Universe Series

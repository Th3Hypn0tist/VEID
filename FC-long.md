VEID — Field-Coupled, Phase-Synchronized Drive (impl. plan v0.3)

GOAL
- Toteuttaa kolmeen massaan perustuva, vaiheistettu sisäliike (X↔Y muunto),
  jossa kuvion asymmetria kytkeytyy väistämättä olemassa olevaan gravitaatiokenttään.
- Ei yritetä “rikkoa” lakeja: mitataan pieni nettidrift/työntö lock-in-tyyppisesti.

AXES & ORIENTATION
- Y-akseli = “kentän suunta” (Maan g), X-akseli = sivuttaissiirron lähde/varasto.
- Rakenteen nollareferenssi on alustaan nähden, mutta mittaus käyttää erillistä inertiareferenssiä.

CORE MECHANICS (v0.1 proto, pöytämalli)
- mC (keskimassa): lineaarikelkka Y-suuntaan, 0.2–1.0 kg, lineaarilaakeri + voice-coil / BLDC-sruuvi.
- mL, mR (sivumassat): kaksi lineaarikelkkaa X-suuntaan (vastakkaissymmetria), 0.2–1.0 kg.
- kXL, kXR (jouset/“varasto”): 5–50 N/m, asetetaan sivumassojen ja keskikelkan väliin.
- CLUTCH_X, CLUTCH_Y: kytkimet jotka voivat olla “FLOAT” (kitka ~min) tai “STIFF” (jäykkä).
  Käytännön ratkaisu: magneettireologinen jarru / eddy-current brake / hammaslukko.
- DAMPERS: säädettävät iskarit (energiantie ulos on mitattava!).
- RUNKO: alumiini, pienikitkaiset lineaarikiskot (HIWIN tms.), kaikki kontaktit mitataan.

SENSORS
- 2× laser-viivamittari (Y-suunta, COM-proxy + rungon y-siirto), 1× optinen rata (X-kelkoille).
- 6D IMU rungossa (proof-of-nothing, ei riitä — vain apudata).
- 2× kapasiitiivinen/optinen etäisyysmajakka inertiaaliseen referenssiin (ripustettu erilleen).
- Pietsoviritin rungossa (monitoroi ääni-/värähtelyvuotoa).

ACTUATORS
- Voice-coil Y: nopea nykäys mC:lle; BLDC+ruuvi käy v0.1:ssä, mutta v0.2:ssa kelkka+VC parempi.
- Servo X: sivumassojen jousipuristus ja palautus; servoprofiilit hallitaan tarkasti.
- Kytkimet: MR-jarruissa PWM-ohjaus (float↔stiff ~millisekunnit).

DRIVE CYCLE (STATE MACHINE)
Tavoite: X-energia → (vaiheenkäännöllä) Y-suunnan asymmetrinen siirto, sitten kytkentä/irrotus oikealla hetkellä.

S0: PRECHARGE_X
- CLUTCH_X=STIFF, CLUTCH_Y=FLOAT
- Purista jousia kXL/kXR: mL→+X, mR→–X (symmetrinen potentiaalivarasto).

S1: Y-KICK (mC boost)
- CLUTCH_X=FLOAT (sivut irti), CLUTCH_Y=STIFF (mC↔runko jäykkä) TAI “virtuaalijäykkä” ohjaimessa.
- Anna mC:lle nopea +Y-nykäys (voice-coil). Sivut eivät “vedä takaisin” tässä hetkessä.

S2: X-RELEASE→Y-COUPLE (vaiheenkäännön ikkuna)
- Synkkaa hetkeen, jolloin mL&mR jouset palautuvat rajusti (X-energia palaamassa).
- CLUTCH_X=STIFF vain mC↔(mL&mR) välillä hetkeksi; CLUTCH_Y=FLOAT (runko irti).
- Tämä “kääntää” X-energian Y-suunnan liikemomentiksi aktiiviselle kolmikolle sisäisesti.

S3: TRIAD→FRAME TRANSFER
- Käännä CLUTCH_Y=STIFF hyvin lyhyeksi ikkunaksi (ms) kun mC:llä on maks. +Y.
- Siirrä impulssi kolmikosta runkoon. Vältä takaisinkytkentää: CLUTCH_X takaisin FLOAT heti.

S4: FLOAT & RESET
- Kaikki FLOAT: anna suhteellisten liikkeiden laantua; mittaa runko-Y.
- Hidas X-PRECHARGE seuraavaa sykliä varten (energiakustannus min).

FREQUENCY & TIMING
- f_drive: 2–20 Hz v0.1:lle (riippuu k ja m). Tavoite: lock-in mittaus taajuudella f_drive.
- Windows: (S2,S3) aikajako mikro-/millisekunneissa; rytmi on koko homman “mojo”.

CONTROL (closed loop)
- Ohjaa f_drive ja ikkunahetket signaalista: “COM-proxy drift @ f_drive” + pietsovärähtely → optimoi vaihetta.
- “Antisherwooding”: vaihda ajoituksen merkki (180°) ja tarkista signaalin kääntyminen.

POWER & LOSSES
- Loggaa P_in (sähkö) vs. mekaaniset työt X/Y:ssä; seuraa lämpö ja akustinen emissio (ne ovat “ulosreittejä”).

BOM (proto v0.1)
- 3× lineaarikelkka (2× ~150 mm X, 1× ~150–200 mm Y), 3× 0.2–1.0 kg massablokit.
- 2× jousi 5–50 N/m, 2× säädettävä iskunvaimennin.
- 2× MR-jarru / eddy-current brake (X), 1× MR-jarru (Y) TAI mekaaninen pikakytkin.
- 1× voice-coil (≥50 N hetkellinen) Y:lle TAI BLDC+ruuvi + jousto-linkki.
- 2× laser-viivamittari (rungon Y), 1× optinen X-mitta, IMU.
- µC/SoC ohjaus (STM32/Teensy + linux SBC), 2× DAC/PWM MR-jarruille.

MEASUREMENT & VALIDATION
- Ripusta koko laite pitkään, matalakitkaiseen heiluriin (torsion tai “kelkka pitkällä ripalla”).
- Aja f_drive ja demoduloi rungon Y-siirtymä lock-in-tyyliin: multiply mittasignaali sin/cos(f_drive), low-pass.
- Tee “A/B”: (a) symmetrinen ajoitus (referenssi, 0-tulos), (b) vaiheistettu ajoitus (VEID).
- Reversoi: käännä Y-suunta (laite 180°) → tuloksen pitäisi vaihtaa merkkiä.
- OFF-resonance-testi: vaihda f_drive ±10–20% → signaalin pitäisi heiketä/flipata.

FALSE POSITIVE KILLERS
- Akustinen työntö: tee mittaus tyhjiökammiolla tai pehmustetussa akustisessa kopissa; loggaa pietsot.
- Lämpökonvektio: tyhjiö tai lämpötila-stabilointi; lyhyet koe-ikkunat.
- Magneettiset reaktiot: ei ferromagneettisia kehyksiä; testaa EQ-kenttä päällä/pois (muutos?).
- Kaapelivoimat: käytä ohuita, löysiä “service loop” -johtoja; toista testit akulla ilman ulkojohtoja.

SCALING (v0.2–v0.3)
- Lisää m (massat) ja k (jäykkyys) jotta f_drive*Δp kasvaa, mutta pidä ikkunat lyhyinä.
- Korvaa mekaaniset kytkimet “virtuaalikytkimillä” (sähkömagneettiset jarrut) → parempi ajoitus.
- Lisää 2. triadi 90° vaiheeseen → jatkuvampi keski-työntö (vector-sum).

THEORY NOTE
- Nettosignaali ~ ∫ (Δmass-distribution • ∇φ) dt syklistä.
- Kenttä on “ulkoisena pankkina”; vaikutus pieni → lock-in on pakollinen.


-- Collider example
select distinct ec.expl, ec.s_lab, ec.o_lab, cp.*
from extraction_colliders ec inner join collider_paths cp on ec.s_obo = cp.path_start and ec.o_obo = cp.path_end 
order by cp.path_start, cp.path_end, cp.path_count, cp.path_step 
;

-- Mediator example
select distinct em.expl, em.s_lab, em.o_lab, mp.*
from extraction_mediators em inner join mediator_paths mp on em.s_obo = mp.path_start and em.o_obo = mp.path_end 
order by mp.path_start, mp.path_end, mp.path_count, mp.path_step 
;


-- Confounder example
select distinct ec.expl, ec.s_lab, ec.o_lab, cp.*
from extraction_confounders ec inner join confounder_paths cp on ec.s_obo = cp.path_start and ec.o_obo = cp.path_end 
order by cp.path_start, cp.path_end, cp.path_count, cp.path_step 
;

-- confounders from the machine reading CUIs to OMOP
select distinct cto1.vocabulary_id s_omop_vocab, cto1.concept_code s_omop_code, cto1.concept_id s_omop_id, 
                cto2.vocabulary_id s_omop_vocab, cto2.concept_code s_omop_code, cto2.concept_id s_omop_id,
                ec.*
from extraction_confounders ec inner join cui_to_omop cto1 on substring(ec.s from '........$') = cto1.cui
   inner join cui_to_omop cto2 on substring(ec.o from '........$') = cto2.cui
limit 10;

-- start and end paths from confounder paths in pheknowlator to OMOP
select distinct ctop1.vocabulary_id s_omop_vocab, ctop1.concept_code s_omop_code, ctop1.concept_id s_omop_id, 
                ctop2.vocabulary_id s_omop_vocab, ctop2.concept_code s_omop_code, ctop2.concept_id s_omop_id,
                cp.*
from confounder_paths cp inner join cui_to_obo cto1 on cp.path_start = cto1.obo inner join cui_to_omop ctop1 on cto1.cui = ctop1.cui 
   inner join cui_to_obo cto2 on cp.path_end = cto2.obo inner join cui_to_omop ctop2 on cto2.cui = ctop2.cui
limit 10;


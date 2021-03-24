import sys
import json
import requests, os
import psycopg2, sys

DEBUG = True

NP_DB_SCHEMA = 'scratch_u54'
NP_DB_TABLE_PREFIX = 'test_srs_np'

#add np to list 
# np = ['KRATOM', 'GREEN TEA', 'GOLDENSEAL', 'CINNAMON', 'CANNABIS', 'LICORICE']

np = ['Glycyrrhiza uralensis','Glycyrrhiza inflata','Mitragyna speciosa', 'Abies alba','Abies borisii','Acacia brevispica','Acacia dealbata','Acacia saligna','Acanthus mollis','Acer floridanum','Acer rubrum','Achillea ageratum','Achillea falcata','Achillea millefolium','Acorus calamus','Actaea racemosa','Acuba sp','Adiantum capillus','Aesculus hippocastanum','Aesculus pavia','Aframomum angustifolium','Aframomum melegueta','Aframomum mildbraedii','Agathosma betulina','Agrimonia eupatoria','Albizia coriaria','Albizia julibrissin','Alcea rosea','Alcea setosa','Alchemilla xanthochlora','Alchornea hirtella','Allium amethystinum','Allium cepa','Allium sp','Alocasia macrorrhizos','Aloe vera','Aloysia citriodora','Alpinia officinarum','Amanita caesarea','Amaranthus spinosus','Ambrosia artemisiifolia','Amomum tsao','Amomum villosum','Amorpha fruticosa','Amsonia ciliata','Amsonia tabernaemontana','Anabasis aretioides','Anacyclus clavatus','Anchusa officinalis','Andropogon glomeratus','Andropogon virginicus','Aneilema beniniense','Aneilema nyasense','Anethum graveolens','Angelica sinensis','Anthyllis vulneraria','Apium graveolens','Aralia racemosa','Aralia spinosa','Arctium lappa','Arctostaphylos uva','Ardisia crenata','Areca catechu','Aristolochia baetica','Aristolochia fimbriata','Aristolochia rugosa','Aristotelia chilensis','Artemisia absinthium','Artemisia annua','Artemisia arborescens','Artemisia herba','Arthrocnemum macrostachyum','Artocarpus altilis','Arum italicum','Arundo donax','Asclepias curassavica','Asclepias erosa','Asclepias incarnata','Asimina angustifolia','Asimina incana','Asimina parviflora','Asparagus acutifolius','Asparagus racemosus','Asphodelus microcarpus','Astragalus monspessulanus','Astragalus propinquus','Atractylodes lancea','Atractylodes macrocephala','Atriplex portulacoides','Azadirachta indica','Bacopa monnieri','Balduina uniflora','Ballota nigra','Baptisia alba','Bauhinia guianensis','Bellardia trixago','Berberis aquifolium','Berberis aristata','Berberis lycium','Berberis vulgaris','Beta vulgaris','Bidens mitis','Bidens pilosa','Bixa orellana','Boehmeria cylindrica','Boletus aereus','Bontia daphnoides','Borago officinalis','Boswelfia serrata','Brassica juncea','Brassica macrocarpa','Brassica oleracea','Brassica rapa','Bryophyllum fedtschenkoi','Bupleurum chinense','Callicarpa americana','Calluna vulgaris','Camellia sinensis','Campsis radicans','Cannabis sativa','Capparis spinosa','Capsella bursa','Carpinus caroliniana','Carthamus lanatus','Carya alba','Carya aquatica','Carya illinoinensis','Carya tomentosa','Cassine buchananii','Castanea dentata','Castanea henryi','Castanea hybrid','Castanea mollissima','Castanea neglecta','Castanea ozarkensis','Castanea pumila','Castanea sativa','Caulophyllum thalictroides','Cecropia peltata','Celtis gomphophylla','Celtis laevigata','Centaurea benedicta','Centaurium erythraea','Centaurium pulchellum','Centranthus ruber','Centrosema virginianum','Cephalanthus occidentalis','Ceratonia siliqua','Cercis canadensis','Cerinthe major','Ceterach officinarum','Chasmanthium latifolium','Chelidonium majus','Chimaphila umbellata','Chionanthus virginicus','Chrysopsis mariana','Cicer incisum','Cichorium intybus','Cinnamomum burmanni','Cinnamomum camphora','Cinnamomum cassia','Cinnamomum verum','Cirsium sp','Cistus creticus','Citrullus ecirrhosus','Citrullus lanatus','Citrus aurantium','Citrus reticulata','Citrus sinensis','Cladium mariscus','Cladonia leporina','Clematis glaucophylla','Clinopodium nepeta','Clinopodium vulgare','Clitoria mariana','Cnidoscolus urens','Codonopsis pilosula','Cola nitida','Coleus forskholii','Combretum molle','Commelina benghalensis','Commelina diffusa','Commiphora mukul','Conyza canadensis','Conyza ramosissima','Coptis chinensis','Cordia curassavica','Cordyceps militaris','Coreopsis major','Coriandrum sativum','Coriolopsis gallica','Cornus florida','Cornus officinalis','Corydalis diphylla','Corylus americana','Corylus avellana','Crassocephalum vitellinum','Crataegus aestivalis','Crataegus azarolus','Crataegus flava','Crataegus laevigata','Crataegus monogyna','Crataegus sp','Crepis neglecta','Crithmum maritimum','Crotalaria juncea','Crotalaria pallida','Croton argyranthemus','Croton echioides','Ctenium aromaticum','Cubitermes ugandensis','Cuminum cyminum','Cuphea carthagenensis','Curcuma Jonga','Curcuma longa','Curcuma zedoaria','Cyclamen hederifolium','Cynometra alexandri','Cyperus rotundus','Daedalea quercina','Daedaleopsis confragosa','Dalea pinnata','Daphne gnidium','Daphne oleoides','Daphne sericea','Daucus carota','Delonix regia','Delphinium fissum','Dianthus rupicola','Digitalis ferruginea','Digitaria cognata','Diodella teres','Dioscorea praehensilis','Dioscorea villosa','Diospyros virginiana','Diplotaxis erucoides','Diplotaxis tenuifolia','Dipsacus fullonum','Ditrysinia fruticosa','Dorylus sp','Drimia pancration','Drosera intermedia','Drypetes ugandensis','Ecballium elaterium','Echinacea angustifolia','Echinacea purpurea','Echium italicum','Eichhornia crassipes','Eleutherococcus senticosus','Elymus repens','Emilia sonchifolia','Encyclia tampensis','Enterolobium cyclocarpum','Epimedium grandif','Epimedium grandiflorum','Epimedium orum','Equisetum hyemale','Equisetum maximum','Erechtites hieracifolia','Erica multiflora','Erigeron strigosus','Eriobotrya japonica','Eriodictyon californicum','Eriogonum tomentosum','Erodium malacoides','Eruca vesicaria','Eryngium foetidum','Erythrina abyssinica','Erythrina herbacea','Erythrina lysistemon','Eschscholzia californica','Eupatorium capillifolium','Eupatorium compositifolium','Eupatorium fortunei','Eupatorium purpureum','Euphorbia antisyphilitica','Euphorbia characias','Euphorbia cyathophora','Euphorbia dendroides','Euphorbia pubentissima','Euphorbia segetalis','Euterpe oleracea','Fagus grandifolia','Ferula communis','Ferula elaeochytris','Ficus carica','Ficus saussureana','Filipendula ulmaria','Fistulina hepatica','Floscopa confusa','Foeniculum vulgare','Fomes fomentarius','Fomitopsis pinicola','Frangula alnus','Fraxinus americana','Fraxinus quadrangulata','Fucus vesiculosus','Fumana thymifolia','Fumaria officinalis','Fuscoporia torulosa','Galactites tomentosa','Galega officinalis','Galium aparine','Galium bermudense','Galium verum','Ganoderma lucidum','Garcinia gummi','Garcinia gummi','Gaylussacia dumosa','Gentiana lutea','Gentiana olivieri','Gentiana tianschanica','Geranium columbinum','Geranium maculatum','Ginkgo biloba','Glaucium flavum','Gloeophyllum sepiarium','Glycine max','Glycyrrhiza glabra','Gnaphalium pensylvanicum','Gnaphalium purpureum','Gratiola virginiana','Grewia calymmatosepala','Gymnema sylvestre','Haloxylon scoparium','Hamamelis virginiana','Handroanthus heptaphyllus','Hapalopilus rutilans','Harpagophytum procumbens','Harungana madagascariensis','Hedera helix','Hedera helix','Helenium amarum','Helianthemum rosmarinifolium','Helichrysum arenarium','Helichrysum panormitanum','Helminthotheca echioides','Herpothallon rubrocinctum','Hesperaloe parviflora','Hibiscus moscheutos','Hippocrepis emerus','Hordeum vulgare','Hydrastis canadensis','Hydrastis canadensis','Hylodesmum repandum','Hylotelephium telephioides','Hymenocallis crassifolia','Hypericum gentianoides','Hypericum hypericoides','Hypericum perforatum','Hypericum piriai','Hypericum punctatum','Hypericum sp','Hyptis verticillata','Hyssopus officinalis','Ilex glabra','Ilex opaca','Ilex paraguariensis','Ilex vomitoria','Indigofera hirsuta','Infundibulicybe geotropa','Inocutis tamaricis','Inonotus obliquus','Inula helenium','Ipomoea cordatotriloba','Ipomoea pandurata','Iris virginica','Jacobaea maritima','Jatropha curcas','Juglans nigra','Juglans regia','Juncus articulatus','Juncus effusus','Juniperus communis','Juniperus oxycedrus','Juniperus virginiana','Kalanchoe mortagei','Khaya anthotheca','Knautia arvensis','Knautia lucana','Lachnanthes caroliniana','Laetiporus sulphureus','Lechea minor','Lechea mucronata','Lechea sessiliflora','Lechea tenuifolia','Leonurus cardiaca','Leopoldia comosa','Lepidium','Lepidium draba','Lepidium meyenii','Lepidium meyenii','Lepidium virginicum','Leucas calostachys','Levisticum officinale','Licania michauxii','Lilium candidum','Limbarda crithmoides','Limonium aegusae','Limonium tenuiculum','Linaria vulgaris','Linum usitatissimum','Liquidambar styraciflua','Liriodendron tulipifera','Lobaria pulmonaria','Lonicera implexa','Lonicera japonica','Lonicera webbiana','Ludwigia erecta','Ludwigia helminthorrhiza','Ludwigia leptocarpa','Ludwigia linearis','Lupinus perennis','Lycium barbarum','Lycopus americanus','Lyonia lucida','Maclura tinctoria','Maesa lanceolata','Magnolia grandiflora','Magnolia officinalis','Magnolia tripetala','Magnolia virginiana','Magydaris pastinacea','Malva sylvestris','Mammea americana','Markhamia lutea','Marrubium vulgare','Marrubium vulgare','Matelea gonocarpos','Matricaria chamomilla','Medicago polymorpha','Melia azedarach','Melilotus albus','Melissa officinalis','Mentha pulegium','Mentha spicata','Meripilus giganteus','Microgramma lycopodioides','Micromeria myrtifolia','Mikania scandens','Mimosa pudica','Mirabilis jalapa','Mitchella repens','Mitracarpus hirtus','Momordica charantia','Momordica sp','Morella cerifera','Morella kandtiana','Morella salicifolia','Morinda citrifolia','Moringa oleifera','Moringa oleifera','Morrenia odorata','Morus rubra','Myriophyllum aquaticum','Myrtus communis','Nectandra coriacea','Nelumbo lutea','Nepeta cataria','Nepeta cilicica','Nephrolepis cordifolia','Nerium oleander','Neurolaena lobata','Nicotiana glauca','Notopterygium incisum','Nuphar lutea','Nymphaea odorata','Ocimum tenuiflorum','Oecophylla longinoda','Oenothera fruticosa','Olea europaea','Ononis spinosa','Oplopanax horridus','Opuntia humifusa','Orbexilum lupinellum','Orchis anthropophora','Orchis italica','Orchis purpurea','Origanum compactum','Origanum ehrenbergii','Origanum libanoticum','Origanum majorana','Origanum syriacum','Origanum vulgare','Origanum vulgare','Oxalis priceae','Oxyria digyna','Panax ginseng','Papaver rhoeas','Papaver somniferum','Parentucellia viscosa','Parietaria judaica','Paronychia argentea','Parthenocissus quinquefolia','Paspalum notatum','Passiflora edulis','Paullinia cupana','Pausinystalia johimbe','Periploca laevigata','Persicaria hydropiperoides','Persicaria punctata','Petroselinum crispum','Peumus boldus','Phagnalon kotschyi','Phillyrea latifolia','Phlomis herba','Phlomis italica','Phlox glaberrima','Phyllanthus amarus','Phytolacca americana','Piloblephis rigida','Pinus echinata','Pinus heldreichii','Pinus mugo','Pinus nigra','Pinus palustris','Pinus peuce','Pinus sylvestris','Piper methysticum','Piper nigrum','Piptoporus betulinus','Piriqueta cistoides','Pistacia lentiscus','Pistacia terebinthus','Pistia stratiotes','Plantago aristata','Plantago major','Plantago virginica','Platanus occidentalis','Plectranthus hadiensis','Pleopeltis polypodioides','Pluchea rosea','Pogostemon cablin','Polygala grandiflora','Polygala nana','Polyporus squamosus','Pontederia cordata','Porodaedalea pini','Posidonia oceanica','Prangos asperula','Prunella vulgaris','Prunus angustifolia','Prunus armeniaca','Prunus caroliniana','Prunus persica','Prunus serotina','Prunus spinosa','Prunus umbellata','Pseudacanthotermes spiniger','Pseudarthria hookeri','Pseudognaphalium obtusifolium','Pseudoscabiosa limonifolia','Pseudotsuga menziesii','Ptelea trifoliata','Pteridium aquilinum','Pyrostegia venusta','Pyrus pashia','Quassia amara','Quercus alba','Quercus arkansana','Quercus cerris','Quercus falcata','Quercus geminata','Quercus ilex','Quercus incana','Quercus inopina','Quercus laevis','Quercus laurifolia','Quercus margaretta','Quercus marilandica','Quercus nigra','Quercus stellata','Quercus virginiana','Ramalina sp','Ranunculus acris','Raphanus raphanistrum','Reynoutria multiflora','Rhamnus lycioides','Rheum','Rheum australe','Rheum palmatum','Rhexia mariana','Rhexia virginica','Rhodiola rosea','Rhus copallinum','Rhus coriaria','Rinorea beniensis','Rivina humilis','Robinia pseudoacacia','Rosa canina','Rosa damascena','Rosa sp','Rosmarinus officinalis','Rubus allegheniensis','Rubus argutus','Rubus cuneifolius','Rubus flagellaris','Rubus laciniatus','Rubus leucodermis','Rubus parvifolius','Rubus praecox','Rubus sp','Rubus trivialis','Rubus ulmifolius','Rubus ursinus','Rudbeckia hirta','Ruellia caroliniensis','Rumex crispus','Rumex hastatulus','Ruscus aculeatus','Ruta chalepensis','Ruta graveolens','Sabal minor','Sagittaria graminea','Salix eriocephala','Salix nigra','Salix × fragilis L.','Salvia officinalis','Salvia pratensis','Salvia sclarea','Salvia sp','Salvia verbenaca','Salvia verticillata','Sambucus canadensis','Sambucus ebulus','Sambucus nigra','Sambucus nigra','Sanguinaria canadensis','Saponaria officinalis','Saposhnikovia divaricata','Sargassum pallidum','Sassafras albidum','Satureja montana','Saururus cernuus','Saussurea gossypiphora','Schinus terebinthifolia','Schisandra chinensis','Schisandra glabra','Schoenoplectus tabernaemontani','Scirpus cyperinus','Scolymus hispanicus','Scrophularia umbrosa','Scutellaria lateriflora','Securidaca longipedunculata','Senecio doriiformis','Senna obtusifolia','Senna occidentalis','Serenoa repens','Sesamum calycinum','Seseli bocconei','Sida spinosa','Sideroxylon celastrinum','Sideroxylon lanuginosum','Silene latifolia','Silene nutans','Silybum marianum','Sisymbrium officinale','Smilax auriculata','Smilax bona','Smilax glauca','Smilax laurifolia','Smilax pumila','Smilax rotundifolia','Smilax smallii','Smyrnium olusatrum','Solanum aculeastrum','Solanum americanum','Solanum anguivi','Solanum carolinense','Solanum linnaeanum','Solanum viarum','Solidago altissima','Solidago canadensis','Solidago odora','Sonchus oleraceus','Spartium junceum','Spermacoce verticillata','Sphagnum L.','Sphagnum sp','Stachys ehrenbergii','Stachys floridana','Stachys germanica','Stachys officinalis','Stachys tymphaea','Sterculia dawei','Stillingia sylvatica','Stylisma aquatica','Stylisma humistrata','Swertia chirata','Swertia petiolata','Symphytum officinale','Syngonanthus flavidulus','Tamarindus indica','Tanacetum falconeri','Tanacetum parthenium','Tanacetum vulgare','Taraxacum officinale','Tephrosia virginiana','Teucrium chamaedrys','Teucrium fruticans','Thapsia garganica','Thelypteris kunthii','Thunbergia fragrans','Thymbra capitata','Thymelaea hirsuta','Thymelaea microphylla','Thymelaea tartonraira','Thymus vulgaris','Tilia × europaea L.','Tillandsia fasciculata','Tillandsia setacea','Tillandsia usneoides','Toddalia asiatica','Tordylium apulum','Trametes versicolor','Tribulus terrestris','Trichaptum biforme','Trifolium badium','Trifolium ochroleucon','Trifolium repens','Trigonelfa foenum','Trigonella foenum','Tripsacum dactyloides','Triticum aestivum','Turnera diffusa','Tussilago farfara','Typha domingensis','Typha latifolia','Ulmus americana','Ulmus minor','Ulmus rubra','Uncaria tomentosa','Urena lobata','Urera trinervis','Urospermum dalechampii','Urtica dioica','Vaccinium arboreum','Vaccinium myrsinites','Vaccinium stamineum','Vaccinium tenellum','Valeriana officinalis','Valeriana officinalis','Vauquelinia californica','Verbascum sinuatum','Verbascum thapsus','Veronica chamaedrys','Viburnum opulus','Vicia cracca','Vicia faba','Vicia sativa','Vinca major','Vitex agnus','Vitis aestivalis','Vitis rotundifolia','Vitis vinifera','Warburgia ugandensis','Wisteria sinensis','Withania somnifera','Withania somnifera','Xanthium strumarium','Youngia japonica','Yucca filamentosa','Zanthoxylum armatum','Zanthoxylum chalybeum','Zanthoxylum clava','Zingiber officinale']

#or specify as argument
#np = [str(sys.argv[1])]

np_result = {}

#Function to query database for structurally diverse substance (kratom, goldenseal, green tea, cinnamon)
#Gets details from tables ix_ginas_substance, ix_ginas_name, ix_ginas_strucdiv, ix_ginas_relationship, 
#ix_ginas_code (for DSLD mapping) 
def get_initial_details(np_item):
        uri = "https://ginas.ncats.nih.gov/ginas/app/api/v1/substances/search?q=" + np_item
        response = requests.get(uri)
        result = response.json()
        if not result["content"]:
                return None
        uuid = result["content"][0]["uuid"]
        substance_class = result["content"][0]["substanceClass"]
        np_result[np_item] = result

        return substance_class

def clean_tables(conn):
        query_clean = ('DROP TABLE IF EXISTS scratch_u54.' + NP_DB_TABLE_PREFIX,
                       'DROP TABLE IF EXISTS scratch_u54.' + NP_DB_TABLE_PREFIX + '_parent',
                       'DROP TABLE IF EXISTS scratch_u54.' + NP_DB_TABLE_PREFIX + '_rel')
        try:
                cur = conn.cursor()
                for query in query_clean:
                        if DEBUG:
                                print(query)
                        cur.execute(query)
                cur.close()
                conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
                cur.close()
                print(error)

def create_tables(conn):
        query_create = ("""
CREATE TABLE scratch_u54.{} (
	dtype varchar(10) NULL,
	substance_uuid varchar(40) NULL,
	created timestamp NULL,
	"class" int4 NULL,
	status varchar(255) NULL,
	modifications_uuid varchar(40) NULL,
	approval_id varchar(20) NULL,
	structure_id varchar(40) NULL,
	structurally_diverse_uuid varchar(40) NULL,
	name_uuid varchar(40) NULL,
	internal_references text NULL,
	owner_uuid varchar(40) NULL,
	"name" varchar(255) NULL,
	"type" varchar(32) NULL,
	preferred bool NULL,
	display_name bool NULL,
	structdiv_uuid varchar(40) NULL,
	source_material_class varchar(255) NULL,
	source_material_state varchar(255) NULL,
	source_material_type varchar(255) NULL,
	organism_family varchar(255) NULL,
	organism_author varchar(255) NULL,
	organism_genus varchar(255) NULL,
	organism_species varchar(255) NULL,
	part_location varchar(255) NULL,
	part text NULL,
	parent_substance_uuid varchar(40) NULL
)
""".format(NP_DB_TABLE_PREFIX), """
CREATE TABLE scratch_u54.{} (
	dtype varchar(10) NULL,
	substance_uuid varchar(40) NULL,
	created timestamp NULL,
	"class" int4 NULL,
	status varchar(255) NULL,
	modifications_uuid varchar(40) NULL,
	approval_id varchar(20) NULL,
	structure_id varchar(40) NULL,
	structurally_diverse_uuid varchar(40) NULL,
	name_uuid varchar(40) NULL,
	internal_references text NULL,
	owner_uuid varchar(40) NULL,
	"name" varchar(255) NULL,
	"type" varchar(32) NULL,
	preferred bool NULL,
	display_name bool NULL,
	structdiv_uuid varchar(40) NULL,
	source_material_class varchar(255) NULL,
	source_material_state varchar(255) NULL,
	source_material_type varchar(255) NULL,
	organism_family varchar(255) NULL,
	organism_author varchar(255) NULL,
	organism_genus varchar(255) NULL,
	organism_species varchar(255) NULL,
	part_location varchar(255) NULL,
	part text NULL,
	parent_substance_uuid varchar(40) NULL
)
""".format(NP_DB_TABLE_PREFIX + "_parent"), """
CREATE TABLE {}.{}_rel (
	uuid varchar(40) NULL,
	current_version int4 NULL,
	created timestamp NULL,
	created_by_id int8 NULL,
	last_edited timestamp NULL,
	last_edited_by_id int8 NULL,
	deprecated bool NULL,
	record_access bytea NULL,
	internal_references text NULL,
	owner_uuid varchar(40) NULL,
	amount_uuid varchar(40) NULL,
	"comments" text NULL,
	interaction_type varchar(255) NULL,
	qualification varchar(255) NULL,
	related_substance_uuid varchar(40) NULL,
	mediator_substance_uuid varchar(40) NULL,
	originator_uuid varchar(255) NULL,
	"type" varchar(255) NULL,
	internal_version int8 NULL
)
""".format(NP_DB_SCHEMA,NP_DB_TABLE_PREFIX))
                        
        try:
                cur = conn.cursor()
                for query in query_create:
                        if DEBUG:
                                print(query)
                        cur.execute(query)
                cur.close()
                conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
                cur.close()
                print(error)
        

def get_structurally_diverse_np(uuid, parent_uuid, conn):
        query_main = """
with np_substance as (
select igs1.uuid as substance_uuid, igs1.* from ix_ginas_substance igs1
where igs1.uuid = '{}'
),
np_strucdiv as (
select * from ix_ginas_strucdiv igs2 
inner join np_substance on np_substance.structurally_diverse_uuid = igs2.uuid 
),
np_parent as (
select igs3.refuuid as parent_uuid from ix_ginas_substanceref igs3 
inner join np_strucdiv on np_strucdiv.parent_substance_uuid = igs3.uuid 
)
insert into {}.{}
select igs.dtype, igs.uuid as substance_uuid, igs.created, igs.class, igs.status, igs.modifications_uuid,
igs.approval_id, igs.structure_id, igs.structurally_diverse_uuid, 
ign.uuid as name_uuid, ign.internal_references, ign.owner_uuid, ign."name",
ign."type", ign.preferred, ign.display_name, 
ixs.uuid as structdiv_uuid, ixs.source_material_class, ixs.source_material_state, ixs.source_material_type,
ixs.organism_family, ixs.organism_author, ixs.organism_genus, ixs.organism_species, ixs.part_location,
ixs.part, ixs.parent_substance_uuid 
from ix_ginas_substance igs 
inner join ix_ginas_name as ign on ign.owner_uuid = igs.uuid 
inner join ix_ginas_strucdiv as ixs on ixs.uuid = igs.structurally_diverse_uuid 
where igs.uuid in 
(select substance_uuid from np_substance) or 
igs.uuid in
(select parent_uuid from np_parent)
""".format(uuid, NP_DB_SCHEMA, NP_DB_TABLE_PREFIX)

        if parent_uuid == '':
                query_parent = None
                query_relations = """
insert into {}.{}_rel 
select *  
from ix_ginas_relationship igr
where igr.owner_uuid = '{}'
""".format(NP_DB_SCHEMA, NP_DB_TABLE_PREFIX, uuid)
        else:
                #do we want all parent synonyms or just single? Should we include a flag for parent in the main query??
                query_parent = """
with np_parent as (
select refuuid as parent_id from ix_ginas_substanceref igs2
where igs2.uuid = '{}'
)
insert into {}.{}_parent
select igs.dtype, igs.uuid as substance_uuid, igs.created, igs.class, igs.status, igs.modifications_uuid,
igs.approval_id, igs.structure_id, igs.structurally_diverse_uuid, 
ign.uuid as name_uuid, ign.internal_references, ign.owner_uuid, ign."name",
ign."type", ign.preferred, ign.display_name, 
ixs.uuid as structdiv_uuid, ixs.source_material_class, ixs.source_material_state, ixs.source_material_type,
ixs.organism_family, ixs.organism_author, ixs.organism_genus, ixs.organism_species, ixs.part_location,
ixs.part, ixs.parent_substance_uuid 
from ix_ginas_substance igs 
inner join ix_ginas_name as ign on ign.owner_uuid = igs.uuid 
inner join ix_ginas_strucdiv as ixs on ixs.uuid = igs.structurally_diverse_uuid 
where igs.uuid in (select parent_id from np_parent)
""".format(parent_uuid, NP_DB_SCHEMA, NP_DB_TABLE_PREFIX)

                query_relations = """
with np_parent as (
select refuuid as parent_id from ix_ginas_substanceref igs2
where igs2.uuid = '{}'
)
insert into {}.{}_rel
select * 
from ix_ginas_relationship igr
where igr.owner_uuid = '{}' or igr.owner_uuid in (select parent_id from np_parent)
""".format(parent_uuid, NP_DB_SCHEMA, NP_DB_TABLE_PREFIX, uuid)

                query_dsld = """
select * from ix_ginas_code igc
where igc.owner_uuid = '{}' and igc.code_system = 'DSLD'
""".format(uuid)

        flag = 0
        try:
                cur = conn.cursor()
                if DEBUG:
                        print(query_main)
                cur.execute(query_main)
                if query_parent is not None:
                        if DEBUG:
                                print(query_parent)
                        cur.execute(query_parent)
                if DEBUG:
                        print(query_relations)
                cur.execute(query_relations)
                cur.close()
                conn.commit()
                flag = 1
        except (Exception, psycopg2.DatabaseError) as error:
                print(error)
        cur.close()
        return flag

#Function to query database for mixture (licorice)
#Gets details from tables ix_ginas_substance, ix_ginas_name, ix_ginas_strucdiv, ix_ginas_relationship, 
#DO components of mixture
def get_mixture_np(uuid, parent_uuid, conn):
        query_main = """
with np_substance as (
select igs1.uuid as substance_uuid, igs1.* from ix_ginas_substance igs1
where igs1.uuid = '{}'
),
np_mixture as (
select * from ix_ginas_mixture igm1
inner join np_substance on np_substance.mixture_uuid = igm1.uuid 
),
np_parent as (
select igs3.refuuid as parent_uuid from ix_ginas_substanceref igs3 
inner join np_mixture on np_mixture.parent_substance_uuid = igs3.uuid 
)
insert into {}.{}_mixture
select igs.dtype, igs.uuid as substance_uuid, igs.created, igs.class, igs.status, igs.modifications_uuid,
igs.approval_id, igs.structure_id, igs.structurally_diverse_uuid, 
ign.uuid as name_uuid, ign.internal_references, ign.owner_uuid, ign."name",
ign."type", ign.preferred, ign.display_name, 
igm.uuid as mixture_uuid, igm.parent_substance_uuid 
from ix_ginas_substance igs 
inner join ix_ginas_name as ign on ign.owner_uuid = igs.uuid 
inner join ix_ginas_mixture as igm on igm.uuid = igs.mixture_uuid 
where igs.uuid in 
(select substance_uuid from np_substance) or 
igs.uuid in
(select parent_uuid from np_parent)
""".format(uuid, NP_DB_SCHEMA, NP_DB_TABLE_PREFIX)
        if parent_uuid == '':
                query_parent = None
                query_relations = """
insert into {}.{}_mixture
select *
from ix_ginas_relationship igr
where igr.owner_uuid = '{}'
""".format(NP_DB_SCHEMA, NP_DB_TABLE_PREFIX,uuid)
        else:
                query_parent = """
with np_parent as (
select refuuid as parent_id from ix_ginas_substanceref igs2
where igs2.uuid = '{}')
insert into {}.{}_parent
select igs.dtype, igs.uuid as substance_uuid, igs.created, igs.class, igs.status, igs.modifications_uuid,
igs.approval_id, igs.structure_id, igs.structurally_diverse_uuid, 
ign.uuid as name_uuid, ign.internal_references, ign.owner_uuid, ign."name",
ign."type", ign.preferred, ign.display_name, 
igm.uuid as mixture_uuid, igm.parent_substance_uuid 
from ix_ginas_substance igs 
inner join ix_ginas_name as ign on ign.owner_uuid = igs.uuid 
inner join ix_ginas_mixture as igm on igm.uuid = igs.mixture_uuid 
where igs.uuid in (select parent_id from np_parent)
""".format(parent_uuid, NP_DB_SCHEMA, NP_DB_TABLE_PREFIX)
                query_relations = """
with np_parent as (
select refuuid as parent_id from ix_ginas_substanceref igs2
where igs2.uuid = '{}')
insert into {}.{}_rel
select * 
from ix_ginas_relationship igr
where igr.owner_uuid = '{}' or igr.owner_uuid in (select parent_id from np_parent)
""".format(parent_uuid, NP_DB_SCHEMA, NP_DB_TABLE_PREFIX, uuid)
                
        '''query_components = """
with np_mixture as (
select igm.uuid from ix_ginas_mixture igm
inner join ix_ginas_substance as igs on igm.uuid = igs.mixture_uuid
where igs.uuid = '{}'),
np_comp_id as (
select igsmc.ix_ginas_component_uuid as comp_uuid from ix_ginas_substance_mix_comp igsmc
inner join np_mixture on np_mixture.uuid = igsmc.ix_ginas_mixture_uuid),
np_component as (
select * from ix_ginas_component igc
inner join ix_ginas_substanceref as iss on igc.substance_uuid = iss.uuid
where igc.uuid in (select comp_uuid from np_comp_id))
insert into {}.{}_mixture_comp
select * from ix_ginas_substance igss
inner join np_component on np_component.approval_id = igss.approval_id
inner join ix_ginas_strucdiv ixs on ixs.uuid = igss.structurally_diverse_uuid
inner join ix_ginas_name as ign on ign.owner_uuid = igss.uuid
""".format(uuid, NP_DB_SCHEMA, NP_DB_TABLE_PREFIX)'''
        
        flag = 0
        try:
                cur = conn.cursor()
                cur.execute(query_main)
                if DEBUG:
                        print(query_main)
                if query_parent is not None:
                        if DEBUG:
                                print(query_parent)
                        cur.execute(query_parent)
                if DEBUG:
                        print(query_relations)
                cur.execute(query_relations)
                cur.close()
                conn.commit()
                flag = 1
        except (Exception, psycopg2.DatabaseError) as error:
                print(error)
        cur.close()
        return flag

if __name__ == '__main__':
        #connect to DB
        try:
                conn = psycopg2.connect("dbname='g_substance_reg' user='rw_grp' host='localhost' password='rw_grp'")
        except Exception as error:
                print(error)
                print('Unable to connect to DB')
                conn = None
        if not conn:
                sys.exit(1)

        #for all items either in NP list or as input, call API to get result as JSON object and get its substance class (structurally diverse, mixture...)
        np_class = {}

        clean_tables(conn)
        create_tables(conn)
        
        for item in np:
                t = get_initial_details(item) 
                if t == None:
                        print('No GSRS results found for: ' + item)
                        print('Trying to URL encode the space')
                        t = get_initial_details(item.replace(' ','%20'))
                        if t == None:
                                print('Trying to URL encode did not work')
                                continue
                        else:
                                np_class[item] = t
                else:
                        np_class[item] = t
                        #print(np_result)
                        
        #based on substance class from above, call function to query the database using the substance ID and parent ID
        for item in np:

                #get substance ID
                if not np_result.get(item):
                        continue

                uuid = np_result[item]["content"][0]["uuid"]
                if 'structurallyDiverse' in np_result[item]["content"][0]:
                        if 'parentSubstance' in np_result[item]["content"][0]['structurallyDiverse']:
                                parent_uuid = np_result[item]["content"][0]["structurallyDiverse"]["parentSubstance"]["uuid"]
                        else:
                                parent_uuid = ''
                elif 'mixture' in np_result[item]['content'][0]:
                        if 'parentSubstance' in np_result[item]['content'][0]['mixture']:
                                parent_uuid = np_result[item]["content"][0]["mixture"]["parentSubstance"]["uuid"]
                        else:
                                parent_uuid = ''

                #if botanical/structurally diverse substance, call function for queries
                if np_class[item] == "structurallyDiverse":
                        flag = get_structurally_diverse_np(uuid, parent_uuid, conn)
                elif np_class[item] == "mixture":
                        flag = get_mixture_np(uuid, parent_uuid, conn)
        if flag:
                print('Success')

        conn.close()



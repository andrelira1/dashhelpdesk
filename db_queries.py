query_1 = """SELECT
-- -----------------------------------------------------------------------
-- -- Consulta Criada BI de indicadores do setor de Helpdesk 	         -----
-- -----------------------------------------------------------------------
	    date_format(t.date,'%Y-%m-%d') as ABERTURA,   
	    day(t.date) DIA_ABERTURA,
	    month(t.date) MES_ABERTURA,
	    year(t.date) ANO_ABERTURA,
	    DATE_FORMAT(t.date,'%Y-%m') AnoMesAbertura,
	    
	    month(t.time_to_resolve) MES_SLA,
	    year(t.time_to_resolve) ANO_SLA,    
	    DATE_FORMAT(t.time_to_resolve,'%Y-%m') AnoMesSla,       
      
       day(t.solvedate) DIA_SOLUCAO,
    	 month(t.solvedate) MES_SOLUCAO,
    	 year(t.solvedate) ANO_SOLUCAO,
    	 DATE_FORMAT(t.solvedate,'%Y-%m') AnoMesSolucao,
    	 t.solvedate							 DataSolucao,
    	 
    	  DAY(t.closedate) 					 DiaFechamento,
    	  MONTH(t.closedate)					 MesFechamento,
    	  YEAR(t.closedate)	  				 AnoFechamento,
    	  -- DATE_FORMAT(t.closedate,'%D/%M/%Y')			 DataFechamento,
    	  t.closedate DataFechamento,
    
    	 upper(g.name) as GRUPO,
    	 upper(ifnull(us.name,'Não Informado')) as TECNICO,
    	 upper(ifnull(us2.name,'Não Informado')) as REQUERENTE,
    	 t.id CHAMADO,
         t.id as TXTTICKET,
    
    	 case when (t.status = 6 or t.status = 5) then  
       	  (case when
          	     -- (date(t.due_date)) >= date(DATE_ADD(t.solvedate, interval ((-1)*(ifnull(rp.TOTAL_HORAS,0)/8)) day ))
              	 	  (date(t.time_to_resolve) >= date(DATE_ADD(t.solvedate, interval ((-1)*(ifnull(rp.TOTAL_HORAS,0)/8)) day )))
              	 	  OR st.id IN (3,4,6,9) -- Customização, Problema Inexistente, Projeto e Falha Operacional não sai do prazo
          		  then 'NO PRAZO' else 'ATRASADO' end
        	  )
    	 else (
       	 -- case when (date(t.due_date)) >= date(DATE_ADD(now(), interval ((-1)*(ifnull(rp.TOTAL_HORAS,0)/8)) day ))
         	   case when (date(t.time_to_resolve) >= date(DATE_ADD(now(), interval ((-1)*(ifnull(rp.TOTAL_HORAS,0)/8)) day )))
         	   			 OR st.id IN (3,4,6,9) -- Customização, Problema Inexistente, Projeto e Falha Operacional não sai do prazo
         	   then 'NO PRAZO' else 'ATRASADO' end
      	   )
   	 
    	 end as STATUS_SLA,
   
       upper(c.completename) as CATEGORIA_COMPLETA,
       upper(c.name) as CATEGORIA,
       upper(c2.name) as CATEGORIA_2,
    	 upper(ifnull(c3.name,c2.name)) as CATEGORIA_3,
    	 upper(ifnull(c4.name,ifnull(c3.name,c2.name))) as CATEGORIA_4,
    	 upper(ifnull(c5.name,ifnull(c4.name,ifnull(c3.name,c2.name)))) as CATEGORIA_5,      
       ROUND ((LENGTH(c.completename) - LENGTH( REPLACE ( c.completename, ">", "") ) ) / LENGTH(">")) qtde_niveis,

       case when ifnull(t.time_to_resolve,0) = 0 then 'S' else 'N' end as SEM_PRAZO,
       case when ifnull(us.name,'X') = 'X' then 'S' else 'N' end as SEM_TECNICO,
       case when t.status = 4 then 'S' else 'N' end as PENDENTE,
       case when ifnull(t.solvedate,0) = 0 then 'N' else 'S' end as SOLUCIONADO,
       case when ifnull(t.closedate,0) = 0 then 'N' else 'S' end as FECHADO,
       case when t.is_deleted = 0 then 'N' else 'S' end as EXCLUIDO,
       upper(ifnull(st.name,'SEM TIPO DE SOLUÇÃO')) as TIPO_SOLUCAO
       
       -- VERDADES 
          -- (t.status = 4)                PENDENTE
          -- ifnull(t.solvedate,0) <> 0	 SOLUCIONADO
          -- ifnull(t.closedate,0) <> 0	 FECHADO
          -- t.is_deleted <> 0				 EXCLUIDO
         
-- ---
       ,modo.name AS MODO
      -- ,modo.id AS IDMODO
       ,CASE WHEN modo.id = 3 THEN 'S' WHEN modo.id <> 3 THEN 'N' END FCR
       ,loc.name AS LOCALIZACAO
       ,CASE WHEN loc.completename LIKE 'Local1%'   THEN 'Local1'
       		 WHEN loc.completename LIKE 'Local2%'  THEN 'Local2'
       		 WHEN loc.completename LIKE 'Local3%' OR loc.completename LIKE 'Local3'
				   OR loc.completename LIKE 'Posto%' OR loc.completename LIKE 'Posto2%'
					   THEN 'Local1'
				 END ORGANIZACAO
				  
		    
       ,CASE WHEN (t.status = 4) AND ifnull(t.solvedate,0) = 0 AND ifnull(t.closedate,0) = 0 AND t.is_deleted = 0						then 'PENDENTE'
       	    WHEN (t.status <> 4) AND ifnull(t.solvedate,0) <> 0 AND ifnull(t.closedate,0) = 0	AND t.is_deleted = 0					then 'SOLUCIONADO'
       	    WHEN (t.status <> 4) AND ifnull(t.solvedate,0) <> 0 AND ifnull(t.closedate,0) <> 0 AND t.is_deleted = 0					then 'FECHADO'
       	    WHEN (t.status <> 4) AND ifnull(t.solvedate,0) = 0 AND ifnull(t.closedate,0) = 0 AND t.is_deleted <> 0					then 'EXCLUIDO'
       	    ELSE 'ABERTO' END SITUACAO
       
		 ,CONCAT('http://localhost/testehelpdesk/front/ticket.form.php?id=', t.id)  AS URL_TICKET-- to_char(t.id))
    
FROM hp_tickets t
		INNER JOIN  hp_itilcategories c 
		  ON(c.id = t.itilcategories_id)
		--  AND(c.id not in(0,1,2,23,24,79,80,83,90))
		--    AND(c.itilcategories_id not in (24,97,102))
		inner join hp_itilcategories c2
		  on(c2.id = c.itilcategories_id)
		left outer join hp_itilcategories c3
		  on(c3.id = c2.itilcategories_id)
		left outer join hp_itilcategories c4
		  on(c4.id = c3.itilcategories_id)
		left outer join hp_itilcategories c5
		  on(c5.id = c4.itilcategories_id)  
		INNER JOIN (
		  select g.tickets_id,
		       g.groups_id
		  from hp_groups_tickets g
		  inner join(
		    select max(g2.id) as id,
		         g2.tickets_id
		       from hp_groups_tickets g2
                          WHERE g2.`type` = 2
		       group by
		        g2.tickets_id  
		  )a  
		      on(a.id = g.id)
		      
		) gt
		  ON(gt.tickets_id = t.id)
		  
		INNER JOIN hp_groups g
		  ON(g.id = gt.groups_id)
		  and(g.id in (2,3,7,13))  -- Código dos Grupos de TIC
                 -- and(g.id in (2,3,7,13,18))  -- Código dos Grupos de TIC
		LEFT OUTER JOIN 
		  (select SUM(d.TOTAL_RP) TOTAL_HORAS,
		      d.id
		  from hp_vw_resumopendente_dq d
		  GROUP BY 
		      d.id
		  ) rp
		  on(rp.id = t.id)
		
		left outer join(
		  select 
		    max(sol.id) as id,
		    sol.items_id,
		    max(sol.solutiontypes_id) as solutiontypes_id
		  from hp_itilsolutions sol 
		  group by  
		    sol.items_id    
		) soli
		  on(soli.items_id = t.id)
		left outer join hp_solutiontypes st 
		  		  ON (st.id = soli.solutiontypes_id) 
		left outer join hp_tickets_users tu
		  		  ON (tu.tickets_id = t.id)
		 and(tu.type = 2)
		left outer join hp_users us
		    	  ON (us.id = tu.users_id)
           --      AND (us.groups_id NOT IN (29)) -- IN (2,3,7,13))
		left outer join hp_tickets_users tu2 
		  		  ON (tu2.tickets_id = t.id)
		    	 AND (tu2.type = 1)
		left outer join hp_users us2
		    	  ON (us2.id   = tu2.users_id)
		LEFT OUTER JOIN hp.hp_locations loc
			 	  ON loc.id		= us2.locations_id
		LEFT OUTER JOIN hp.hp_solutiontemplates modo
				  ON modo.solutiontypes_id	=  st.id
				 AND modo.id = 3

where t.date>= '2020-07-01'
  AND us.groups_id <> 29;"""


query_2 = """SELECT
-- -----------------------------------------------------------------------
-- -- Consulta Criada BI de indicadores do setor de Helpdesk 	         -----
-- -----------------------------------------------------------------------
	    t.date as ABERTURA,   
	    day(t.date) DIA_ABERTURA,
	    month(t.date) MES_ABERTURA,
	    year(t.date) ANO_ABERTURA,
	    DATE_FORMAT(t.date,'%Y-%m') AnoMesAbertura,
	    
	    month(t.time_to_resolve) MES_SLA,
	    year(t.time_to_resolve) ANO_SLA,    
	    DATE_FORMAT(t.time_to_resolve,'%Y-%m') AnoMesSla,       
      
       day(t.solvedate) DIA_SOLUCAO,
    	 month(t.solvedate) MES_SOLUCAO,
    	 year(t.solvedate) ANO_SOLUCAO,
    	 DATE_FORMAT(t.solvedate,'%Y-%m') AnoMesSolucao,
    	 t.solvedate							 DataSolucao,
    	 
    	  DAY(t.closedate) 					 DiaFechamento,
    	  MONTH(t.closedate)					 MesFechamento,
    	  YEAR(t.closedate)	  				 AnoFechamento,
    	  -- DATE_FORMAT(t.closedate,'%D/%M/%Y')			 DataFechamento,
    	  t.closedate DataFechamento,
    
    	 upper(g.name) as GRUPO,
    	 upper(ifnull(us.name,'Não Informado')) as TECNICO,
    	 upper(ifnull(us2.name,'Não Informado')) as REQUERENTE,
    	 t.id CHAMADO,
         t.id as TXTTICKET,
    
    	 case when (t.status = 6 or t.status = 5) then  
       	  (case when
          	     -- (date(t.due_date)) >= date(DATE_ADD(t.solvedate, interval ((-1)*(ifnull(rp.TOTAL_HORAS,0)/8)) day ))
              	 	  (date(t.time_to_resolve) >= date(DATE_ADD(t.solvedate, interval ((-1)*(ifnull(rp.TOTAL_HORAS,0)/8)) day )))
              	 	  OR st.id IN (3,4,6,9) -- Customização, Problema Inexistente, Projeto e Falha Operacional não sai do prazo
          		  then 'NO PRAZO' else 'ATRASADO' end
        	  )
    	 else (
       	 -- case when (date(t.due_date)) >= date(DATE_ADD(now(), interval ((-1)*(ifnull(rp.TOTAL_HORAS,0)/8)) day ))
         	   case when (date(t.time_to_resolve) >= date(DATE_ADD(now(), interval ((-1)*(ifnull(rp.TOTAL_HORAS,0)/8)) day )))
         	   			 OR st.id IN (3,4,6,9) -- Customização, Problema Inexistente, Projeto e Falha Operacional não sai do prazo
         	   then 'NO PRAZO' else 'ATRASADO' end
      	   )
   	 
    	 end as STATUS_SLA,
   
       upper(c.completename) as CATEGORIA_COMPLETA,
       upper(c.name) as CATEGORIA,
       upper(c2.name) as CATEGORIA_2,
    	 upper(ifnull(c3.name,c2.name)) as CATEGORIA_3,
    	 upper(ifnull(c4.name,ifnull(c3.name,c2.name))) as CATEGORIA_4,
    	 upper(ifnull(c5.name,ifnull(c4.name,ifnull(c3.name,c2.name)))) as CATEGORIA_5,      
       ROUND ((LENGTH(c.completename) - LENGTH( REPLACE ( c.completename, ">", "") ) ) / LENGTH(">")) qtde_niveis,

       case when ifnull(t.time_to_resolve,0) = 0 then 'S' else 'N' end as SEM_PRAZO,
       case when ifnull(us.name,'X') = 'X' then 'S' else 'N' end as SEM_TECNICO,
       case when t.status = 4 then 'S' else 'N' end as PENDENTE,
       case when ifnull(t.solvedate,0) = 0 then 'N' else 'S' end as SOLUCIONADO,
       case when ifnull(t.closedate,0) = 0 then 'N' else 'S' end as FECHADO,
       case when t.is_deleted = 0 then 'N' else 'S' end as EXCLUIDO,
       upper(ifnull(st.name,'SEM TIPO DE SOLUÇÃO')) as TIPO_SOLUCAO
       
       -- VERDADES 
          -- (t.status = 4)                PENDENTE
          -- ifnull(t.solvedate,0) <> 0	 SOLUCIONADO
          -- ifnull(t.closedate,0) <> 0	 FECHADO
          -- t.is_deleted <> 0				 EXCLUIDO
         
-- ---
       ,modo.name AS MODO
      -- ,modo.id AS IDMODO
       ,CASE WHEN modo.id = 3 THEN 'S' WHEN modo.id <> 3 THEN 'N' END FCR
       ,loc.name AS LOCALIZACAO
       ,CASE WHEN loc.completename LIKE 'Local1%'   THEN 'Local1'
       		 WHEN loc.completename LIKE 'Local2%'  THEN 'Local2'
       		 WHEN loc.completename LIKE 'Local3%' OR loc.completename LIKE 'Local3%'
				   OR loc.completename LIKE 'POSTO1%' OR loc.completename LIKE 'Posto2%'
					   THEN 'Local1'
				 END ORGANIZACAO
				  
		    
       ,CASE WHEN (t.status = 4) AND ifnull(t.solvedate,0) = 0 AND ifnull(t.closedate,0) = 0 AND t.is_deleted = 0						then 'PENDENTE'
       	    WHEN (t.status <> 4) AND ifnull(t.solvedate,0) <> 0 AND ifnull(t.closedate,0) = 0	AND t.is_deleted = 0					then 'SOLUCIONADO'
       	    WHEN (t.status <> 4) AND ifnull(t.solvedate,0) <> 0 AND ifnull(t.closedate,0) <> 0 AND t.is_deleted = 0					then 'FECHADO'
       	    WHEN (t.status <> 4) AND ifnull(t.solvedate,0) = 0 AND ifnull(t.closedate,0) = 0 AND t.is_deleted <> 0					then 'EXCLUIDO'
       	    ELSE 'ABERTO' END SITUACAO
       
		 ,CONCAT('http://localhost/testehelpdesk/front/ticket.form.php?id=', t.id)  AS URL_TICKET-- to_char(t.id))
    
FROM hp_tickets t
		INNER JOIN  hp_itilcategories c 
		  ON(c.id = t.itilcategories_id)
		--  AND(c.id not in(0,1,2,23,24,79,80,83,90))
		--    AND(c.itilcategories_id not in (24,97,102))
		inner join hp_itilcategories c2
		  on(c2.id = c.itilcategories_id)
		left outer join hp_itilcategories c3
		  on(c3.id = c2.itilcategories_id)
		left outer join hp_itilcategories c4
		  on(c4.id = c3.itilcategories_id)
		left outer join hp_itilcategories c5
		  on(c5.id = c4.itilcategories_id)  
		INNER JOIN (
		  select g.tickets_id,
		       g.groups_id
		  from hp_groups_tickets g
		  inner join(
		    select max(g2.id) as id,
		         g2.tickets_id
		       from hp_groups_tickets g2
                          WHERE g2.`type` = 2
		       group by
		        g2.tickets_id  
		  )a  
		      on(a.id = g.id)
		      
		) gt
		  ON(gt.tickets_id = t.id)
		  
		INNER JOIN hp_groups g
		  ON(g.id = gt.groups_id)
		  and(g.id in (2,3,7,13))  -- Código dos Grupos de TIC
                 -- and(g.id in (2,3,7,13,18))  -- Código dos Grupos de TIC
		LEFT OUTER JOIN 
		  (select SUM(d.TOTAL_RP) TOTAL_HORAS,
		      d.id
		  from hp_vw_resumopendente_dq d
		  GROUP BY 
		      d.id
		  ) rp
		  on(rp.id = t.id)
		
		left outer join(
		  select 
		    max(sol.id) as id,
		    sol.items_id,
		    max(sol.solutiontypes_id) as solutiontypes_id
		  from hp_itilsolutions sol 
		  group by  
		    sol.items_id    
		) soli
		  on(soli.items_id = t.id)
		left outer join hp_solutiontypes st 
		  		  ON (st.id = soli.solutiontypes_id) 
		left outer join hp_tickets_users tu
		  		  ON (tu.tickets_id = t.id)
		 and(tu.type = 2)
		left outer join hp_users us
		    	  ON (us.id = tu.users_id)
            --     AND (us.groups_id NOT IN (29) -- IN (2,3,7,13)) 
		left outer join hp_tickets_users tu2 
		  		  ON (tu2.tickets_id = t.id)
		    	 AND (tu2.type = 1)
		left outer join hp_users us2
		    	  ON (us2.id   = tu2.users_id)
		LEFT OUTER JOIN hp.hp_locations loc
			 	  ON loc.id		= us2.locations_id
		LEFT OUTER JOIN hp.hp_solutiontemplates modo
				  ON modo.solutiontypes_id	=  st.id
				 AND modo.id = 3

where t.date>= '2020-07-01'
  AND us.groups_id <> 29;"""
/* --- FRANCHISE FACT --- */

DROP TABLE IF EXISTS franchise_fact CASCADE;

CREATE TABLE franchise_fact
(
   ffid           integer       NOT NULL,
   franchise_id   integer       NOT NULL,
   week_id        integer       NOT NULL,
   opponent_id    integer,
   matchup_type   varchar(50)   NOT NULL,
   result         varchar(50),
   total_score    numeric       NOT NULL,
   oponent_score  numeric
);


COMMIT;

/* --- PFR BRIDGE --- */

DROP TABLE IF EXISTS pfr_bridge CASCADE;

CREATE TABLE pfr_bridge
(
   pfr_id  varchar(30),
   mfl_id  float8
);

COMMIT;


/* --- PLAYER FACT --- */

DROP TABLE IF EXISTS player_fact CASCADE;

CREATE TABLE player_fact
(
   pfid           serial,
   player_id      integer       NOT NULL,
   week_id        integer       NOT NULL,
   franchise_id   integer,
   roster_status  varchar(50),
   actual_status  varchar(50),
   score          numeric
);


COMMIT;

/* --- WEEK DIM --- */

DROP TABLE IF EXISTS week_dim CASCADE;

CREATE TABLE week_dim
(
   week_id     integer   NOT NULL,
   year        integer   NOT NULL,
   week        integer   NOT NULL,
   start_date  date      NOT NULL,
   end_date    date      NOT NULL
);

COMMIT;

ALTER TABLE week_dim
   ADD CONSTRAINT week_dim_pkey1
   PRIMARY KEY (week_id);

ALTER TABLE franchise_fact
   ADD CONSTRAINT franchise_fact_pkey
   PRIMARY KEY (ffid);
   
ALTER TABLE player_fact
   ADD CONSTRAINT player_fact_pkey
   PRIMARY KEY (pfid);

ALTER TABLE franchise_fact
  ADD CONSTRAINT fk_franchise_id FOREIGN KEY (franchise_id)
  REFERENCES contracts_franchise (franchise_id)
  ON UPDATE NO ACTION
  ON DELETE NO ACTION;

ALTER TABLE franchise_fact
  ADD CONSTRAINT fk_week_id FOREIGN KEY (week_id)
  REFERENCES week_dim (week_id)
  ON UPDATE NO ACTION
  ON DELETE NO ACTION;

ALTER TABLE player_fact
  ADD CONSTRAINT fk_franchise_id FOREIGN KEY (franchise_id)
  REFERENCES contracts_franchise (franchise_id)
  ON UPDATE NO ACTION
  ON DELETE NO ACTION;

ALTER TABLE player_fact
  ADD CONSTRAINT fk_player_id FOREIGN KEY (player_id)
  REFERENCES contracts_player (player_id)
  ON UPDATE NO ACTION
  ON DELETE NO ACTION;

ALTER TABLE player_fact
  ADD CONSTRAINT fk_week_id FOREIGN KEY (week_id)
  REFERENCES week_dim (week_id)
  ON UPDATE NO ACTION
  ON DELETE NO ACTION;
  
COMMIT;

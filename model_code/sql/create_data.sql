CREATE TABLE if not exists uir.data (
        nuclide int4,
        temperature int4,
        reaction_102_fast float,
        reaction_103_fast float,
        reaction_102_warm float,
        reaction_103_warm float,
        run_time TIMESTAMP NOT NULL DEFAULT clock_timestamp(),
        PRIMARY KEY (nuclide, temperature)
);

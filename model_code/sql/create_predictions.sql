CREATE TABLE if not exists uir.predicts (
        nuclide int4,
        temperature int4,
        reaction_102_fast float,
        reaction_103_fast float,
        reaction_102_warm float,
        reaction_103_warm float,
        metric_value_102_fast float,
        metric_value_103_fast float,
        metric_value_102_warm float,
        metric_value_103_warm float,
        run_time TIMESTAMP NOT NULL DEFAULT clock_timestamp()
)
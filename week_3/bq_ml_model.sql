-- CREATE OR REPLACE TABLE `trips_data_all.yellow_tripdata_ml` (
--   `passenger_count` INTEGER,
--   `trip_distance` FLOAT64,
--   `PULocationID` STRING,
--   `DOLocationID` STRING,
--   `payment_type` STRING,
--   `fare_amount` FLOAT64,
--   `tolls_amount` FLOAT64,
--   `tip_amount` FLOAT64
-- ) AS (
--   SELECT passenger_count, trip_distance, CAST(PULocationID AS STRING), CAST(DOLocationID AS STRING), CAST(payment_type AS STRING), fare_amount, tolls_amount, tip_amount
--   FROM `trips_data_all.external_table`
--   WHERE fare_amount != 0
-- );


-- CREATE OR REPLACE MODEL `trips_data_all.tip_model`
-- OPTIONS (
--   model_type='linear_reg',
--   input_label_cols=['tip_amount'],
--   DATA_SPLIT_METHOD='AUTO_SPLIT'
-- ) AS
-- SELECT
--   *
-- FROM
--   `trips_data_all.yellow_tripdata_ml`
-- WHERE
--   tip_amount IS NOT NULL;

-- CREATE OR REPLACE TABLE st_temp.total_visit_metrics_xtra44_march22_starters_wlabel5_mod4_bq_model (
--   `first_day_dt` DATE,
--   `first_visits` INT64,
--   `first_page_views` INT64,
--   `dy_0_visits` INT64,
--   `dy_1_visits` INT64,
--   `dy_2_visits` INT64,
--   `dy_3_visits` INT64,
--   `dy_4_visits` INT64,
--   `dy_5_visits` INT64,
--   `dy_6_visits` INT64,
--   `dy_7_visits` INT64,
--   `label` STRING
-- ) AS (
--   SELECT first_day_dt, first_visits, first_page_views, dy_0_visits,dy_1_visits, dy_2_visits, 
-- dy_3_visits, dy_4_visits, dy_5_visits,dy_6_visits, dy_7_visits, label
--   FROM st_temp.total_visit_metrics_xtra44_june21_starters_wlabel5_mod4
-- );

-- CREATE OR REPLACE MODEL `i-dss-sports-data.st_temp.app_predictor_model_march_2022_BQ_many_metrics`
-- OPTIONS(
--   model_type='LOGISTIC_REG',
--   input_label_cols=['label']
-- ) AS 
-- -- SELECT first_day_dt, first_visits, first_page_views, dy_0_visits,dy_1_visits, dy_2_visits, 
-- -- dy_3_visits, dy_4_visits, dy_5_visits,dy_6_visits, dy_7_visits, label
-- SELECT weekday, week, hour, dy_part, device_os, sport_mlb,	sport_nba,	sport_ncaab,	sport_ncaaf,	sport_nfl,	sport_nhl,
-- page_type_scoring, page_type_information, page_type_navigation, page_type_stories, page_type_odds_picks ,page_type_standings,
-- first_notifications,	first_breaking_news,	first_top_stories,	first_favorites, first_video_plays, first_video_mins,
-- dy_0_pvs,	dy_1_pvs,	dy_2_pvs,	dy_3_pvs,	dy_4_pvs,	dy_5_pvs,	dy_6_pvs,	dy_7_pvs,	month_page_views,	dy_0_vps,	dy_1_vps,	dy_2_vps,	dy_3_vps,	dy_4_vps,	dy_5_vps,	dy_6_vps,	dy_7_vps,	month_video_plays,	month_media_starts,	dy_0_time_spent,	dy_1_time_spent,	dy_2_time_spent,	dy_3_time_spent,	dy_4_time_spent,	dy_5_time_spent,	dy_6_time_spent	dy_7_time_spent,
-- first_day_dt, first_visits, first_page_views, dy_0_visits,dy_1_visits, dy_2_visits, 
-- dy_3_visits, dy_4_visits, dy_5_visits,dy_6_visits, dy_7_visits, label
--   FROM st_temp.total_visit_metrics_xtra44_june21_starters_wlabel5_mod4;

SELECT *
FROM ML.EXPLAIN_PREDICT(
MODEL `i-dss-sports-data.st_temp.app_predictor_model_march_2022_BQ_many_metrics`, (
    SELECT
      *
    FROM
      st_temp.total_visit_metrics_xtra44_june22_starters_wlabel5_mod4
  ), STRUCT(5 as top_k_features)
);
\encoding UTF8
SET search_path TO process_eer, public;

-- ===== Dataset =====
WITH new_object AS (
    INSERT INTO object (object_type)
    SELECT 'dataset'
    WHERE NOT EXISTS (  /*如果不存在 → 才建立 object → 再建立子類資料*/
        SELECT 1
        FROM dataset
        WHERE dataset_name = 'AI4I 2020'
    )
    RETURNING oid
)
INSERT INTO dataset (
    oid,
    dataset_name,
    source,
    version,
    description
)
SELECT
    oid,
    'AI4I 2020',
    'UCI Machine Learning Repository',
    'v1',
    'Predictive maintenance dataset used for machine failure prediction.'
FROM new_object;


-- ===== Model =====
WITH new_object AS (
    INSERT INTO object (object_type)
    SELECT 'model'
    WHERE NOT EXISTS (
        SELECT 1
        FROM model
        WHERE model_name = 'AI4I Failure Predictor'
    )
    RETURNING oid
)
INSERT INTO model (
    oid,
    model_name,
    algorithm,
    version,
    description
)
SELECT
    oid,
    'AI4I Failure Predictor',
    'Logistic Regression',
    'v1',
    'Baseline model for machine failure prediction.'
FROM new_object;


-- ===== AnalysisRun =====
WITH new_object AS (
    INSERT INTO object (object_type)
    SELECT 'analysis_run'
    WHERE NOT EXISTS (
        SELECT 1
        FROM analysis_run r,
             dataset d,
             model m
        WHERE r.dataset_oid = d.oid
          AND r.model_oid = m.oid
          AND d.dataset_name = 'AI4I 2020'
          AND m.model_name = 'AI4I Failure Predictor'
          AND r.threshold = 0.5000
          AND r.status = 'completed'
    )
    RETURNING oid
)
INSERT INTO analysis_run (
    oid,
    dataset_oid,
    model_oid,
    threshold,
    status
)
SELECT
    new_object.oid,
    d.oid,
    m.oid,
    0.5000,
    'completed'
FROM new_object,
     dataset d,
     model m
WHERE d.dataset_name = 'AI4I 2020'
  AND m.model_name = 'AI4I Failure Predictor';
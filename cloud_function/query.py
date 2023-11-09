ACCOUNT_LEVEL_QUERY = """
WITH
  max_date AS (
  SELECT
    MAX(month_start) AS max_date
  FROM
    `poetic-dock-367718.publishing.monthly_periodic_asset_portfolio` ),
  monthly_periodic_cashflows AS (
  SELECT
    acc.account_name,
    DATE_ADD(gla.date, INTERVAL 1 DAY) AS date,
    CASE
      WHEN gla.end_balance_amount_pounds > 0 THEN CASE
      WHEN acc.account_currency = 'Pound' THEN gla.end_balance_amount_pounds
    ELSE
    gla.end_balance_amount_euros
  END
    ELSE
    0
  END
    AS inflow,
    CASE
      WHEN gla.end_balance_amount_pounds < 0 THEN CASE
      WHEN acc.account_currency = 'Pound' THEN - gla.end_balance_amount_pounds
    ELSE
    - gla.end_balance_amount_euros
  END
    ELSE
    0
  END
    AS outflow
  FROM
    `poetic-dock-367718.dw_accounting.accounts` acc
  INNER JOIN
    `poetic-dock-367718.dw_accounting.gl_monthly_periodic_snapshot` gla
  ON
    gla.account_id = acc.account_id
  WHERE
    acc.account_family = 'Stock Market'
    AND gla.ledger_book_name = 'Accounting App')
SELECT
  ass.account_name AS entity_name,
  ass.month_start AS date,
  CASE
    WHEN ass.account_currency = 'Pound' THEN ass.end_balance_amount_pounds
  ELSE
  ass.end_balance_amount_euros
END
  AS value,
  COALESCE(pas.inflow, 0) AS inflow,
  COALESCE(pas.outflow,0) AS outflow
FROM
  `poetic-dock-367718.publishing.monthly_periodic_asset_portfolio` ass
LEFT JOIN
  monthly_periodic_cashflows pas
ON
  ass.month_start = pas.date
  AND ass.account_name = pas.account_name
CROSS JOIN
  max_date md
WHERE
  ass.account_family = 'Stock Market'
  AND ass.month_start <= md.max_date
  AND ass.month_start NOT IN ('2023-06-01',
    '2023-07-01',
    '2023-08-01',
    '2023-09-01',
    '2023-10-01')
  AND NOT ( ass.account_name = 'DeGiro - IPCO' AND ass.month_start = '2019-04-01' )
UNION ALL
SELECT
  ass.account_name AS entity_name,
  pas.date,
  CASE
    WHEN ass.account_currency = 'Pound' THEN ass.end_balance_amount_pounds
  ELSE
  ass.end_balance_amount_euros
END
  AS value,
  COALESCE(pas.inflow, 0) AS inflow,
  COALESCE(pas.outflow,0) AS outflow
FROM (
  SELECT
    *
  FROM
    `poetic-dock-367718.publishing.monthly_periodic_asset_portfolio`
  WHERE
    month_start = '2023-05-01'
    AND account_family = 'Stock Market' ) ass
RIGHT JOIN (
  SELECT
    acc.account_name,
    DATE_ADD(gla.date, INTERVAL 1 DAY) AS date,
    CASE
      WHEN gla.end_balance_amount_pounds > 0 THEN CASE
      WHEN acc.account_currency = 'Pound' THEN gla.end_balance_amount_pounds
    ELSE
    gla.end_balance_amount_euros
  END
    ELSE
    0
  END
    AS inflow,
    CASE
      WHEN gla.end_balance_amount_pounds < 0 THEN CASE
      WHEN acc.account_currency = 'Pound' THEN - gla.end_balance_amount_pounds
    ELSE
    - gla.end_balance_amount_euros
  END
    ELSE
    0
  END
    AS outflow
  FROM
    `poetic-dock-367718.dw_accounting.accounts` acc
  INNER JOIN
    `poetic-dock-367718.dw_accounting.gl_monthly_periodic_snapshot` gla
  ON
    gla.account_id = acc.account_id
  WHERE
    acc.account_family = 'Stock Market'
    AND gla.ledger_book_name = 'Accounting App'
    AND DATE_ADD(gla.date, INTERVAL 1 DAY) IN ('2023-06-01',
      '2023-07-01',
      '2023-08-01',
      '2023-09-01',
      '2023-10-01')) pas
ON
  ass.account_name = pas.account_name
INNER JOIN (
  SELECT
    account_name,
    MIN(month_start) AS min_date,
    MAX(month_start) AS max_date
  FROM
    `poetic-dock-367718.publishing.monthly_periodic_asset_portfolio`
  WHERE
    account_family = 'Stock Market'
  GROUP BY
    account_name) md
ON
  md.account_name = pas.account_name
  AND pas.date <= md.max_date
  AND pas.date >= md.min_date;
"""
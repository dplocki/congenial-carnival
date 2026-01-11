# Good Old Games

## Reading the galaxy.db

The location of the file: `c:\ProgramData\GOG.com\Galaxy\storage\galaxy-2.0.db`.

The SQL query:

```sql
SELECT
    DISTINCT json_extract(GP_TITLE.value, '$.title') AS title,
    PPD.purchaseDate,
    COALESCE(GT.minutesInGame, 0) AS minutesPlayed,
    LPD.lastPlayedDate,
    GP_TITLE.releaseKey
FROM
    ProductPurchaseDates PPD
    JOIN GamePieces GP_TITLE ON PPD.gameReleaseKey = GP_TITLE.releaseKey
        AND GP_TITLE.gamePieceTypeId = (SELECT id FROM GamePieceTypes WHERE TYPE='title')
    LEFT JOIN GameTimes GT ON GT.releaseKey = GP_TITLE.releaseKey
    LEFT JOIN LastPlayedDates LPD ON LPD.gameReleaseKey = GP_TITLE.releaseKey
WHERE
    GP_TITLE.releaseKey NOT IN (SELECT
        DISTINCT REPLACE(REPLACE(REPLACE(json_each.value, '"', ''), '[', ''), ']', '') AS dlcKey
        FROM GamePieces GP_DLC
        CROSS JOIN json_each(json_extract(GP_DLC.value, '$.dlcs'))
        WHERE GP_DLC.gamePieceTypeId = (SELECT
            id
            FROM GamePieceTypes
            WHERE TYPE='dlcs')
        AND GP_DLC.value IS NOT NULL
        AND GP_DLC.value NOT IN ('{"dlcs":null}', '{"dlcs":[]}'))
    AND GP_TITLE.value NOT LIKE 'dlc%'
    AND GP_TITLE.value IS NOT NULL
    AND GP_TITLE.value != ''
ORDER BY title ASC
```

### Problems

* data are scattered
* not only games, also packs etc.

### Other

* Other project reading GoG Galaxy library: https://github.com/AB1908/GOG-Galaxy-Export-Script/

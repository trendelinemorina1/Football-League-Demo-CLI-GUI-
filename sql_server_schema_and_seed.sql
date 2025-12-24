

SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
GO

------------------------------------------------------------
-- 1. Drop existing tables (if you want a clean setup)
------------------------------------------------------------
IF OBJECT_ID('dbo.matches', 'U') IS NOT NULL
    DROP TABLE dbo.matches;
GO

IF OBJECT_ID('dbo.users', 'U') IS NOT NULL
    DROP TABLE dbo.users;
GO

------------------------------------------------------------
-- 2. Create table: users
------------------------------------------------------------
CREATE TABLE dbo.users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(256) NOT NULL UNIQUE,
    [password] NVARCHAR(256) NOT NULL
);
GO

------------------------------------------------------------
-- 3. Create table: matches
------------------------------------------------------------
CREATE TABLE dbo.matches (
    id INT IDENTITY(1,1) PRIMARY KEY,
    home_team NVARCHAR(128) NOT NULL,
    away_team NVARCHAR(128) NOT NULL,
    kickoff_datetime DATETIME NOT NULL,
    status NVARCHAR(32) NOT NULL, -- played, live, upcoming
    home_score INT NOT NULL CONSTRAINT DF_matches_home_score DEFAULT (0),
    away_score INT NOT NULL CONSTRAINT DF_matches_away_score DEFAULT (0)
);
GO

------------------------------------------------------------
-- 4. Seed default user (if table is empty)
------------------------------------------------------------
IF NOT EXISTS (SELECT 1 FROM dbo.users)
BEGIN
    INSERT INTO dbo.users (username, [password])
    VALUES (N'lina@gmail.com', N'demodemo');
END;
GO

------------------------------------------------------------
-- 5. Seed sample Serie A matches (if table is empty)
------------------------------------------------------------
IF NOT EXISTS (SELECT 1 FROM dbo.matches)
BEGIN
    INSERT INTO dbo.matches
        (home_team, away_team, kickoff_datetime, status, home_score, away_score)
    VALUES
        -- Played matches
        (N'Inter Milan', N'AC Milan',  CONVERT(DATETIME, '2025-01-10 20:45', 120), N'played',  2, 1),
        (N'Juventus',    N'Napoli',    CONVERT(DATETIME, '2025-01-11 18:00', 120), N'played',  1, 1),

        -- Live matches
        (N'Roma',        N'Lazio',     CONVERT(DATETIME, '2025-01-12 21:00', 120), N'live',    0, 0),
        (N'Atalanta',    N'Fiorentina',CONVERT(DATETIME, '2025-01-12 21:00', 120), N'live',    1, 0),

        -- Upcoming matches
        (N'Udinese',     N'Bologna',   CONVERT(DATETIME, '2025-01-20 18:30', 120), N'upcoming',0, 0),
        (N'Torino',      N'Genoa',     CONVERT(DATETIME, '2025-01-21 20:45', 120), N'upcoming',0, 0);
END;
GO



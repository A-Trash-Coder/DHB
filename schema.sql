CREATE TABLE IF NOT EXISTS modlog (
    guildid BIGINT NOT NULL,
    channelid BIGINT NOT NULL,
    logamounts INT NOT NULL
);

CREATE TABLE IF NOT EXISTS modcases (
    guildid BIGINT NOT NULL,
    casenumber INT NOT NULL,
    casetype TEXT NOT NULL,
    caseuserid BIGINT NOT NULL,
    casemodid BIGINT NOT NULL,
    casereason TEXT NOT NULL,
    logmsgid BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS warns (
    userid BIGINT NOT NULL,
    guildid BIGINT NOT NULL,
    modid BIGINT NOT NULL,
    modname TEXT NOT NULL,
    reason TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS lightswitch (
    guildid BIGINT NOT NULL,
    automoderation BOOL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS automodsettings (
    guildid BIGINT NOT NULL,
    discordinvites BOOL DEFAULT TRUE,
    cursewords BOOL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS cursewords (
    guildid BIGINT NOT NULL,
    word TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS loggingsettings (
    guildid BIGINT NOT NULL,
    channelid BIGINT NOT NULL,
    message_delete BOOL DEFAULT TRUE,
    member_join BOOL DEFAULT TRUE,
    member_leave BOOL DEFAULT TRUE,
    member_ban BOOL DEFAULT TRUE,
    member_unban BOOL DEFAULT TRUE,
    channel_create BOOL DEFAULT TRUE,
    channel_delete BOOL DEFAULT TRUE,
    role_create BOOL DEFAULT TRUE,
    role_delete BOOL DEFAULT TRUE,
    bulk_message_delete BOOL DEFAULT TRUE,
    message_edit BOOL DEFAULT TRUE
);
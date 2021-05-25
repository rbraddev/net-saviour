CREATE MIGRATION m1tauy2iukzeawjajaovg3exk4riiuv7sokljxteq6botkx4kdxm3a
    ONTO initial
{
  CREATE MODULE inventory IF NOT EXISTS;
  CREATE MODULE util IF NOT EXISTS;
  CREATE SCALAR TYPE util::IP EXTENDING std::str {
      CREATE CONSTRAINT std::regexp(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$');
  };
  CREATE ABSTRACT TYPE inventory::Device {
      CREATE REQUIRED PROPERTY hostname -> std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY ip -> util::IP {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE PROPERTY site -> std::str;
      CREATE INDEX ON (__subject__.hostname);
      CREATE INDEX ON (__subject__.ip);
  };
  CREATE TYPE inventory::Interface {
      CREATE PROPERTY description -> std::str;
      CREATE PROPERTY ip -> util::IP;
      CREATE REQUIRED PROPERTY mac -> std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE PROPERTY macs -> array<std::str>;
      CREATE REQUIRED PROPERTY name -> std::str;
  };
  CREATE TYPE inventory::Desktop EXTENDING inventory::Device {
      CREATE REQUIRED PROPERTY mac -> std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE INDEX ON (__subject__.mac);
      CREATE REQUIRED LINK interface -> inventory::Interface;
  };
  CREATE TYPE inventory::NetworkDevice EXTENDING inventory::Device {
      CREATE MULTI LINK interfaces -> inventory::Interface;
      CREATE REQUIRED PROPERTY nodeid -> std::int64 {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE INDEX ON (__subject__.nodeid);
      CREATE REQUIRED PROPERTY active -> std::bool {
          SET default := true;
      };
      CREATE PROPERTY image -> std::str;
  };
};

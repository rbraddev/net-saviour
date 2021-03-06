CREATE MIGRATION m1btix2nxsg5wan4dakql4y5cn5vaxboemwlnpgnej66rddmmqbpyq
    ONTO initial
{
  CREATE MODULE inventory IF NOT EXISTS;
  CREATE MODULE util IF NOT EXISTS;
  CREATE SCALAR TYPE util::IP EXTENDING std::str {
      CREATE CONSTRAINT std::regexp(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$');
  };
  CREATE ABSTRACT TYPE inventory::Device {
      CREATE REQUIRED PROPERTY active -> std::bool {
          SET default := true;
      };
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
  CREATE TYPE inventory::Desktop EXTENDING inventory::Device {
      CREATE REQUIRED PROPERTY mac -> std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE INDEX ON (__subject__.mac);
      CREATE PROPERTY cidr -> std::int16;
      CREATE REQUIRED PROPERTY nodeid -> std::int64 {
          CREATE CONSTRAINT std::exclusive;
      };
  };
  CREATE TYPE inventory::Interface {
      CREATE LINK desktop -> inventory::Desktop;
      CREATE REQUIRED PROPERTY mac -> std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE INDEX ON (__subject__.mac);
      CREATE PROPERTY ip -> util::IP;
      CREATE INDEX ON (__subject__.ip);
      CREATE PROPERTY cidr -> std::int16;
      CREATE PROPERTY description -> std::str;
      CREATE REQUIRED PROPERTY name -> std::str;
      CREATE PROPERTY vlan -> std::int16;
  };
  CREATE TYPE inventory::NetworkDevice EXTENDING inventory::Device {
      CREATE MULTI LINK interfaces -> inventory::Interface {
          ON TARGET DELETE  ALLOW;
      };
      CREATE REQUIRED PROPERTY nodeid -> std::int64 {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE INDEX ON (__subject__.nodeid);
      CREATE PROPERTY device_type -> std::str;
      CREATE PROPERTY image -> std::str;
      CREATE PROPERTY model -> std::str;
      CREATE PROPERTY platform -> std::str;
  };
};

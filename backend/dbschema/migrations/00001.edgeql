CREATE MIGRATION m1cavgnegroiozc5lvsixauiduwqxv4x5pfq7gpc3wp6uixjibo3aq
    ONTO initial
{
  CREATE MODULE inventory IF NOT EXISTS;
  CREATE TYPE inventory::NetworkDevice {
      CREATE REQUIRED PROPERTY hostname -> std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE PROPERTY image -> std::str;
      CREATE REQUIRED PROPERTY ip -> std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY nodeid -> std::int64 {
          CREATE CONSTRAINT std::exclusive;
      };
  };
  CREATE TYPE inventory::Desktop {
      CREATE LINK switch -> inventory::NetworkDevice;
      CREATE REQUIRED PROPERTY hostname -> std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY ip -> std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE PROPERTY switch_port -> std::str;
  };
};

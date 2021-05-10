CREATE MIGRATION m1fq36irignbl5piowcbfojnlsoxvzlx3ezx62w5kcmktewwrzl5ia
    ONTO initial
{
  CREATE MODULE inventory IF NOT EXISTS;
  CREATE TYPE inventory::NetworkDevice {
      CREATE REQUIRED PROPERTY hostname -> std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE PROPERTY image2 -> std::str;
      CREATE PROPERTY image3 -> std::str;
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

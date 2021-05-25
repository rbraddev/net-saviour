CREATE MIGRATION m1lpawfu4huyrnftgvt3fmi2lmd64ppbeqpkng44iwm3ux3aqlx4ma
    ONTO m1myxgbqqhin764n6kil36k35hsnd6nmrbjn7mwkvqcg4wy3c7tipq
{
  ALTER TYPE inventory::Desktop {
      DROP LINK interface;
  };
  ALTER TYPE inventory::Interface {
      CREATE LINK desktop -> inventory::Desktop;
  };
  ALTER TYPE inventory::Interface {
      DROP PROPERTY connected;
  };
  ALTER TYPE inventory::NetworkDevice {
      CREATE PROPERTY model -> std::str;
  };
};

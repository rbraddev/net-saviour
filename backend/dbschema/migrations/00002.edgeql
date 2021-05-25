CREATE MIGRATION m1myxgbqqhin764n6kil36k35hsnd6nmrbjn7mwkvqcg4wy3c7tipq
    ONTO m1tauy2iukzeawjajaovg3exk4riiuv7sokljxteq6botkx4kdxm3a
{
  ALTER TYPE inventory::Interface {
      ALTER PROPERTY macs {
          RENAME TO connected;
      };
  };
};

CREATE MIGRATION m1twtfez6nl3lucyh2zgkjbkfj3utmcuqhgpyca2qj4spczponzpfa
    ONTO m1fq36irignbl5piowcbfojnlsoxvzlx3ezx62w5kcmktewwrzl5ia
{
  ALTER TYPE inventory::NetworkDevice {
      DROP PROPERTY image2;
      DROP PROPERTY image3;
  };
};

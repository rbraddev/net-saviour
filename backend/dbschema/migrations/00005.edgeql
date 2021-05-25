CREATE MIGRATION m12h3kd4j7yyraihlore4hnveezxgtl5abxt5v6gczeb4gg6e7a5ba
    ONTO m1i5d4nwls62nk5oge2wk26zofbi7phylzxqp6b46m2ftgh4oe2ojq
{
  ALTER TYPE inventory::Interface {
      CREATE INDEX ON (__subject__.mac);
  };
};

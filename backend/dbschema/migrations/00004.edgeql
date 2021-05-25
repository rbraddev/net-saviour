CREATE MIGRATION m1i5d4nwls62nk5oge2wk26zofbi7phylzxqp6b46m2ftgh4oe2ojq
    ONTO m1lpawfu4huyrnftgvt3fmi2lmd64ppbeqpkng44iwm3ux3aqlx4ma
{
  ALTER TYPE inventory::Interface {
      CREATE PROPERTY subnet -> std::int16;
  };
};

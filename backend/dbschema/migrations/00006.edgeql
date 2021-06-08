CREATE MIGRATION m1nlh6hw4n3cwrupnglipdueznhcqrqhm5lggmzn7qx7e2texwnj2q
    ONTO m12h3kd4j7yyraihlore4hnveezxgtl5abxt5v6gczeb4gg6e7a5ba
{
  ALTER TYPE inventory::Interface {
      CREATE INDEX ON (__subject__.ip);
  };
};

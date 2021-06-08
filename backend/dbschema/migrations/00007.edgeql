CREATE MIGRATION m1xxyu2gyrgchfd7aketcuhlhrpn4xf4ljhdfmguzs6xxcd2eoeyna
    ONTO m1nlh6hw4n3cwrupnglipdueznhcqrqhm5lggmzn7qx7e2texwnj2q
{
  ALTER TYPE inventory::Interface {
      ALTER PROPERTY ip {
          CREATE CONSTRAINT std::exclusive;
      };
  };
};

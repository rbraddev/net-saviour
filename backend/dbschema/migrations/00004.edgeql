CREATE MIGRATION m1zpphv6ivalbzdhiopc6crkkllamcr7pz3k3tn74o6wirbpec57aa
    ONTO m1jm5dthh76b2jzjihpx4b6e5slnluwuo4fyxtobthwp33vfsl6vpa
{
  ALTER TYPE inventory::Interface {
      CREATE PROPERTY vlan -> std::int16;
  };
};

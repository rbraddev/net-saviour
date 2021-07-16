CREATE MIGRATION m1yxvaodwlqhdlbkkquttu4xfa32zld2d3oernttzzi7khda6afzhq
    ONTO m1btix2nxsg5wan4dakql4y5cn5vaxboemwlnpgnej66rddmmqbpyq
{
  ALTER TYPE inventory::Desktop {
      ALTER PROPERTY nodeid {
          SET TYPE std::int16;
      };
  };
  ALTER TYPE inventory::NetworkDevice {
      ALTER PROPERTY nodeid {
          SET TYPE std::int16;
      };
  };
};

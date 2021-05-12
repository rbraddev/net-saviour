CREATE MIGRATION m1qn3yyfnml2yz5gcojj3r5b5rigzoeppnr3axiyvpme2dto6bkrgq
    ONTO m1cavgnegroiozc5lvsixauiduwqxv4x5pfq7gpc3wp6uixjibo3aq
{
  ALTER TYPE inventory::NetworkDevice {
      CREATE REQUIRED PROPERTY active -> std::bool {
          SET default := true;
      };
  };
};

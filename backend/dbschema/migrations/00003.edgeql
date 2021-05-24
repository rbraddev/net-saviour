CREATE MIGRATION m1tclsk6pfsluokp47i5dwmxfocvnrrqykqstl5sxbyvmie2hq3o3a
    ONTO m1qn3yyfnml2yz5gcojj3r5b5rigzoeppnr3axiyvpme2dto6bkrgq
{
  ALTER TYPE inventory::Desktop {
      CREATE INDEX ON (__subject__.hostname);
      CREATE INDEX ON (__subject__.ip);
  };
  ALTER TYPE inventory::NetworkDevice {
      CREATE INDEX ON (__subject__.nodeid);
      CREATE INDEX ON (__subject__.ip);
  };
};

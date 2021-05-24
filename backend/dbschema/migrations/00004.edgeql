CREATE MIGRATION m17qscwosafjmomqeojbt5xb4sgve2udhwl7gev5oenia3phjrgkca
    ONTO m1tclsk6pfsluokp47i5dwmxfocvnrrqykqstl5sxbyvmie2hq3o3a
{
  ALTER TYPE inventory::Desktop {
      CREATE REQUIRED PROPERTY mac -> std::str {
          SET REQUIRED USING ('xxxxxxxxxxxx');
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE INDEX ON (__subject__.mac);
  };
  ALTER TYPE inventory::NetworkDevice {
      CREATE PROPERTY site -> std::str;
  };
};

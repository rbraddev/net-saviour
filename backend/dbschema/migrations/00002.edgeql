CREATE MIGRATION m1l4hzcmeypqxs5bvqplmnucipkf6nvsehfvkx6qxzzrp45h3zo3iq
    ONTO m1dfoth6drm5pfrwnb2lx7cf2zwlvqvxsuuqk76w5wed3xkxidzpca
{
  ALTER TYPE inventory::Device {
      CREATE REQUIRED PROPERTY active -> std::bool {
          SET default := true;
      };
  };
  ALTER TYPE inventory::NetworkDevice {
      ALTER PROPERTY active {
          RESET OPTIONALITY;
          DROP OWNED;
          RESET TYPE;
      };
  };
};

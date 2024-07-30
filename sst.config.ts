import type { SSTConfig } from "sst";
import { SvelteKitSite } from "sst/constructs";

export default {
  config(_input) {
    return {
      name: "state-govt-employment-explorer",
      region: "us-east-1",
    };
  },
  stacks(app) {
    app.stack(function Site({ stack }) {
      const site = new SvelteKitSite(stack, "site", {
        customDomain: {
          domainName: "aspep.grupovisual.org",
          hostedZone: "grupovisual.org",
        }
      });
      stack.addOutputs({
        url: site.url,
      });
    });
  },
} satisfies SSTConfig;

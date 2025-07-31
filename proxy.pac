function FindProxyForURL(url, host) {
  const domains = ["whatismyipaddress.com","x.com", "cloudflare.com"];
  for (let i = 0; i < domains.length; i++) {
    if (host === domains[i] || host.endsWith("." + domains[i])) {
      return "PROXY 185.195.71.218:41843";
    }
  }
  return "DIRECT";
}
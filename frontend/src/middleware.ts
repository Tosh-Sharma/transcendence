export { default } from "next-auth/middleware";

export const config = {
  matcher: [
    "/protected-route-example",
    "/pages-mentioned-here-are-protected",
    "/me",
    "/",
  ],
};

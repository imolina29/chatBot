module.exports = {
  BrowserRouter: ({ children }) => children,
  Routes: ({ children }) => children,
  Route: ({ element }) => element,
  Link: ({ children }) => <span>{children}</span>,
  useNavigate: () => () => {},
};
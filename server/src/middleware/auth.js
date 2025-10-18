export const requireAuth = (req, res, next) => {
  if (!req.session || !req.session.userId) {
    return res.status(401).json({
      success: false,
      error: { message: 'Authentication required' },
    });
  }
  next();
};

export const optionalAuth = (req, res, next) => {
  // For endpoints that work with or without auth
  next();
};

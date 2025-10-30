import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { auth } from '../utils/api';
import { useStore } from '../store/store';
import Button from '../components/Common/Button';
import Input from '../components/Common/Input';
import { Brain } from 'lucide-react';

export default function Register() {
  const navigate = useNavigate();
  const setUser = useStore((state) => state.setUser);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    fullName: '',
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const validate = () => {
    const newErrors = {};

    if (formData.username.length < 3) {
      newErrors.username = 'Username must be at least 3 characters';
    }

    if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Invalid email address';
    }

    if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validate()) {
      return;
    }

    setLoading(true);

    try {
      const response = await auth.register({
        username: formData.username,
        email: formData.email,
        password: formData.password,
        fullName: formData.fullName || null,
      });
      setUser(response.data.data.user);
      navigate('/chat');
    } catch (err) {
      setErrors({
        submit: err.response?.data?.error?.message || 'Registration failed',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    // Clear error for this field
    if (errors[e.target.name]) {
      setErrors({
        ...errors,
        [e.target.name]: '',
      });
    }
  };

  return (
    <div className="h-full flex items-center justify-center p-3 sm:p-4 lg:p-6 overflow-y-auto">
      <div className="w-full max-w-[90%] sm:max-w-md lg:max-w-lg 2xl:max-w-2xl">
        <div className="bg-bg-secondary/70 backdrop-blur-xl border border-border-primary rounded-xl sm:rounded-2xl p-5 sm:p-8 lg:p-10 2xl:p-12 shadow-2xl">
          {/* Logo */}
          <div className="flex justify-center mb-6 sm:mb-8 lg:mb-10">
            <div className="w-12 h-12 sm:w-16 sm:h-16 lg:w-20 lg:h-20 2xl:w-24 2xl:h-24 bg-gradient-to-br from-primary to-accent-1 rounded-xl sm:rounded-2xl flex items-center justify-center">
              <Brain className="w-6 h-6 sm:w-8 sm:h-8 lg:w-10 lg:h-10 2xl:w-12 2xl:h-12 text-white" />
            </div>
          </div>

          {/* Title */}
          <h1 className="text-2xl sm:text-3xl lg:text-4xl 2xl:text-5xl font-bold text-center mb-2 sm:mb-3">Create Account</h1>
          <p className="text-sm sm:text-base lg:text-lg 2xl:text-xl text-text-secondary text-center mb-6 sm:mb-8 lg:mb-10">
            Sign up to start using Think AI
          </p>

          {/* Error Message */}
          {errors.submit && (
            <div className="mb-4 sm:mb-5 lg:mb-6 p-2.5 sm:p-3 lg:p-4 bg-red-500/10 border border-red-500/50 rounded-lg text-red-500 text-xs sm:text-sm lg:text-base">
              {errors.submit}
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-3 sm:space-y-4 lg:space-y-5">
            <Input
              label="Username"
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              placeholder="Choose a username"
              error={errors.username}
              required
              autoFocus
            />

            <Input
              label="Email"
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="your@email.com"
              error={errors.email}
              required
            />

            <Input
              label="Full Name (Optional)"
              type="text"
              name="fullName"
              value={formData.fullName}
              onChange={handleChange}
              placeholder="Your full name"
            />

            <Input
              label="Password"
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Create a password"
              error={errors.password}
              required
            />

            <Input
              label="Confirm Password"
              type="password"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              placeholder="Confirm your password"
              error={errors.confirmPassword}
              required
            />

            <Button
              type="submit"
              variant="primary"
              className="w-full"
              disabled={loading}
            >
              {loading ? 'Creating account...' : 'Create Account'}
            </Button>
          </form>

          {/* Login Link */}
          <p className="mt-4 sm:mt-6 lg:mt-8 text-center text-text-secondary text-xs sm:text-sm lg:text-base 2xl:text-lg">
            Already have an account?{' '}
            <Link to="/login" className="text-primary hover:underline font-medium">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}

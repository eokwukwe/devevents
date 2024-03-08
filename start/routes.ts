import router from '@adonisjs/core/services/router'
import { middleware } from './kernel.js'

const EventsController = () => import('#controllers/events/events_controller')
const LoginController = () => import('#controllers/auth/login_controller')
const UsersController = () => import('#controllers/users/users_controller')
const CategoriesController = () => import('#controllers/events/categories_controller')

router.get('/', async () => {
  return {
    message: 'Welcome to Devevents AdonisJS API!',
  }
})

// Auth resource
router.post('/auth/login', [LoginController]).as('auth.login')

router.get('/events/categories', [CategoriesController, 'index']).as('events.categories')

// Users resource
router
  .resource('users', UsersController)
  .apiOnly()
  .only(['index', 'store', 'show', 'update'])
  .use(['index', 'show', 'update'], middleware.auth())

// Events resource
router
  .resource('events', EventsController)
  .only(['index', 'store', 'show', 'update', 'destroy'])
  .use(['store', 'update', 'destroy'], middleware.auth())

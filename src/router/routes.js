const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', 
        component: () => import('pages/IndexPage.vue'),
        meta: {
          title: 'Football Charts',
          description: '🚨 The first data load may take up to one minute.'
        }
      },
      { 
        path: 'average-stats', 
        component: () => import('src/pages/tables/AverageStats.vue'),
        meta: {
          title: 'Average Stats',
          description: 'Average performance of all teams in a given league.'
        }
      },
      { 
        path: 'position-history', 
        component: () => import('src/pages/tables/PositionHistory.vue'),
        meta: {
          title: 'Position History',
          description: 'Comparison of teams in the same league that finished in a given position.'
        }
      },
      { 
        path: 'promoted-teams', 
        component: () => import('src/pages/tables/PromotedTeams.vue'),
        meta: {
          title: 'Promoted Teams',
          description: 'Performance of promoted teams in the season after promotion.'
        }
      },
      { 
        path: 'season-standings', 
        component: () => import('src/pages/tables/SeasonStandings.vue'),
        meta: {
          title: 'Season Standings',
          description: 'Final table of any league and season.'
        }
      },
      { 
        path: 'team-trajectory', 
        component: () => import('src/pages/tables/TeamTrajectory.vue'),
        meta: {
          title: 'Team Trajectory',
          description: 'Results of a given team over every season.'
        }
      },
      { 
        path: 'position-frequency', 
        component: () => import('src/pages/pie_charts/PositionFrequency.vue'),
        meta: {
          title: 'Position Frequency',
          description: 'Number of times that teams in the same league finished in a given position.'
        }
      },
      { 
        path: 'promotion-frequency', 
        component: () => import('src/pages/bar_charts/PromotionFrequency.vue'),
        meta: {
          title: 'Promotion Frequency',
          description: 'Number of times that teams have been promoted to a given league.'
        }
      },
      { 
        path: 'relegation-frequency', 
        component: () => import('src/pages/bar_charts/RelegationFrequency.vue'),
        meta: {
          title: 'Relegation Frequency',
          description: 'Number of times that teams have been relegated from a given league.'
        }
      },
    ],
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
]

export default routes

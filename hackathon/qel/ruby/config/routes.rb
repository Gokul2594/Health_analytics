Rails.application.routes.draw do
  resources :users
  post 'login' => 'users#login'
  get 'login' => 'users#login_new'
  get 'complete_test' => 'users#complete_test'
  post 'create_complete_test' => 'users#create_complete_test'
  get 'display_result/:hemogram/:bio/:lipid/:liver' => 'users#display_result'
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end

#include "configuration.h"

/*--------------------------------------------------------------------------------------------------------------*/
/*										Timer Configuration														*/
/*--------------------------------------------------------------------------------------------------------------*/

/* Fonction permettant la configuration du choix du timer ainsi que sa fréqunce */
void Timer_Config(TIM_HandleTypeDef * Timer, TIM_TypeDef * timePort, uint16_t prescaler, uint16_t period){
	TIM_MasterConfigTypeDef TimerMaster;

	/* Acivation du timer mis en paramètre */
	ENABLE_CLK_TIMER_PORT(timePort);

	/* configuration du timer */
	Timer->Instance = timePort;
	Timer->Init.CounterMode = TIM_COUNTERMODE_UP;
	Timer->Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
	Timer->Init.Prescaler = (prescaler);
	Timer->Init.Period = period;

	/* Initialisation du Timer */
	HAL_TIM_Base_Init(Timer);

	/* Initialization du timer Maitre */
	TimerMaster.MasterOutputTrigger = TIM_TRGO_ENABLE;
	TimerMaster.MasterSlaveMode = TIM_MASTERSLAVEMODE_ENABLE;
	HAL_TIMEx_MasterConfigSynchronization(Timer, &TimerMaster);
}

/* Fonction permettant de configurer le mode PWM pour le timer */
void Timer_Mode_PWM_Config(TIM_HandleTypeDef * Timer, TIM_OC_InitTypeDef *TIM_PWM_OC, uint16_t mode, uint16_t polarity){

	/* Configuration du timer mis en paramètre pour le mode PWM */
	HAL_TIM_PWM_Init(Timer);

	/* Configure le mode du timer */
	TIM_PWM_OC->OCMode = mode;

	/* Configure la polarité */
	TIM_PWM_OC->OCPolarity = polarity;
}

/*Fonction permettant de gérer le rapport cyclique du channel */
void Timer_PWM_Pulse_Channel(TIM_HandleTypeDef * Timer, TIM_OC_InitTypeDef *TIM_PWM_OC , uint16_t channel, uint16_t pulse){

	TIM_PWM_OC->Pulse = pulse;
	HAL_TIM_OC_ConfigChannel(Timer, TIM_PWM_OC, channel);
}

void ENABLE_CLK_TIMER_PORT(TIM_TypeDef * timer){
	if(timer == TIM1)
		__HAL_RCC_TIM1_CLK_ENABLE();
	else if(timer == TIM2)
		__HAL_RCC_TIM2_CLK_ENABLE();
	else if(timer == TIM3)
		__HAL_RCC_TIM3_CLK_ENABLE();
	else if(timer == TIM4)
		__HAL_RCC_TIM4_CLK_ENABLE();
	else if(timer == TIM5)
		__HAL_RCC_TIM5_CLK_ENABLE();
	else if(timer == TIM6)
		__HAL_RCC_TIM6_CLK_ENABLE();
	else if(timer == TIM7)
		__HAL_RCC_TIM7_CLK_ENABLE();
	else if(timer == TIM8)
		__HAL_RCC_TIM8_CLK_ENABLE();
	else if(timer == TIM9)
		__HAL_RCC_TIM9_CLK_ENABLE();
	else if(timer == TIM10)
		__HAL_RCC_TIM10_CLK_ENABLE();
	else if(timer == TIM11)
		__HAL_RCC_TIM11_CLK_ENABLE();
	else if(timer == TIM12)
		__HAL_RCC_TIM12_CLK_ENABLE();
	else if(timer == TIM13)
		__HAL_RCC_TIM13_CLK_ENABLE();
	else if(timer == TIM14)
		__HAL_RCC_TIM14_CLK_ENABLE();
}

/*--------------------------------------------------------------------------------------------------------------*/
/*									GPIO Configuration															*/
/*--------------------------------------------------------------------------------------------------------------*/

/* Fonction permettant la configuration de l'horloge des ports */
void GPIO_Configuration(GPIO_TypeDef * GPIO, uint16_t mode, uint16_t Pin){
	/* Activation de l'horloge du port */
	ENABLE_CLK_GPIO_PORT(GPIO);

	GPIO_InitTypeDef GPIO_Config;

	/* Configuration du mode */
	GPIO_Config.Mode = mode;

	/* Configuration des pins */
	GPIO_Config.Pin = Pin;

	/*Initialisation de la configuration */
	HAL_GPIO_Init(GPIO, &GPIO_Config);
}

void GPIO_Configuration_Alternate(GPIO_TypeDef * GPIO, uint16_t mode, uint16_t Pin, uint16_t alternate){
	/* Activation de l'horloge du port */
	ENABLE_CLK_GPIO_PORT(GPIO);

	GPIO_InitTypeDef GPIO_Config;

	/* Configuration du mode */
	GPIO_Config.Mode = mode;
	GPIO_Config.Alternate = alternate;

	/* Configuration des pins */
	GPIO_Config.Pin = Pin;

	/*Initialisation de la configuration */
	HAL_GPIO_Init(GPIO, &GPIO_Config);
}

/* Permet d'activer l'horloge du port */
void ENABLE_CLK_GPIO_PORT(GPIO_TypeDef *GPIO){
	if(GPIO == GPIOA)
		__HAL_RCC_GPIOA_CLK_ENABLE();
	else if(GPIO == GPIOB)
		__HAL_RCC_GPIOB_CLK_ENABLE();
	else if(GPIO == GPIOC)
		__HAL_RCC_GPIOC_CLK_ENABLE();
	else if(GPIO == GPIOD)
		__HAL_RCC_GPIOD_CLK_ENABLE();
	else if(GPIO == GPIOE)
		__HAL_RCC_GPIOE_CLK_ENABLE();
	else if(GPIO == GPIOF)
		__HAL_RCC_GPIOF_CLK_ENABLE();
	else if(GPIO == GPIOG)
		__HAL_RCC_GPIOG_CLK_ENABLE();
	else if(GPIO == GPIOH)
		__HAL_RCC_GPIOH_CLK_ENABLE();
}

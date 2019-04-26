#ifndef CONFIGURATION_H_
#define CONFIGURATION_H_

#include "stm32f4xx_hal.h"

#define LED_PORT	GPIOD
#define GREEN		GPIO_PIN_12
#define ORANGE		GPIO_PIN_13
#define RED			GPIO_PIN_14
#define BLUE 		GPIO_PIN_15
#define BUTTON0		GPIO_PIN_0
#define TIMER4		4
#define LED_ALL		GREEN | ORANGE | RED | BLUE
#define GRE_ORA		GREEN | ORANGE
#define BLU_RED		BLUE | RED

void Timer_Mode_PWM_Config(TIM_HandleTypeDef * Timer, TIM_OC_InitTypeDef *TIM_PWM_OC, uint16_t mode, uint16_t polarity);
void Timer_PWM_Pulse_Channel(TIM_HandleTypeDef * Timer, TIM_OC_InitTypeDef *TIM_PWM_OC , uint16_t channel, uint16_t pulse);
void ENABLE_CLK_TIMER_PORT(TIM_TypeDef * timer);
void Timer_Config(TIM_HandleTypeDef * Timer, TIM_TypeDef * timePort, uint16_t prescaler, uint16_t period);
void Timer_Mode_IC_Config(TIM_HandleTypeDef * Timer, uint16_t polarity, uint16_t filter, uint16_t selection, uint16_t prescaler);
void ENABLE_CLK_GPIO_PORT(GPIO_TypeDef * GPIO);
void GPIO_Configuration(GPIO_TypeDef * GPIO, uint16_t mode, uint16_t Pin);

#endif

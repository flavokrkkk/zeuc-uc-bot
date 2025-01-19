from sqlalchemy import select
from backend.database.models.models import Discount, Reward
from backend.database.models.models import UCCode




async def test_db(session):
    try:
        db_exist = (await session.execute(select(UCCode))).scalars().all()
        if db_exist:
            await session.close()
            return
        
        uc_codes_values = [60, 325, 660, 1200, 1800, 3850, 8100, 10200]
        
        uc_codes = []
        rewards = []
        for value in uc_codes_values:
            uc_codes.append(UCCode(code=f"uc_code_{value}", value=value))
        for uc_code in uc_codes[:3]:
            rewards.append(
                Reward(
                    reward_type="uc_code",
                    uc_code=uc_code
                )
            )
        
        discounts = {100: 1000, 200: 2000, 300: 300, 500: 5000}
        for key, value in discounts.items():
            rewards.append(
                Reward(
                    reward_type="discount", 
                    discount=Discount(
                        value=key, 
                        min_payment_value=value
                    )
                )
            )

        session.add_all(uc_codes)
        session.add_all(rewards)
        await session.commit()
        await session.close()
    except Exception as e:
        print(e)
    finally:
        await session.close()
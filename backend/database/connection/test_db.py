from sqlalchemy import select
from backend.database.models.models import Discount, Price, Reward, User
from backend.database.models.models import UCCode


async def test_db(session):
    try:
        db_exist = (await session.execute(select(UCCode))).scalars().all()
        if db_exist:
            await session.close()
            return
        
        test_user = User(tg_id=1,username="test")
        test_referer = User(tg_id=2,username="test_referer")
        
        uc_codes_values = {60: [100, 1], 325: [200, 4], 660: [300, 5], 1800: [2000, 8], 3850: [5500, 10], 8100: [10000, 20]}
        
        uc_codes = []
        rewards = []
        for key, value in uc_codes_values.items():
            uc_codes.append(
                UCCode(
                    code=f"uc_code_{value}", 
                    ucinitial=key, 
                    price_per_uc=Price(
                        price=value[0], 
                        point=value[1]
                    )
                )
            )
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
        session.add(test_user)
        session.add(test_referer)
        await session.commit()
        await session.close()
    except Exception as e:
        print(e)
    finally:
        await session.close()